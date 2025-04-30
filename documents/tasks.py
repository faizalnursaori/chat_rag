import json

from huey.contrib.djhuey import task
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings

from core.ai.chromadb import chroma, openai_ef
from core.ai.mistral import mistral
from core.ai.prompt_manager import PromptManager
from documents.models import DOC_STATUS_COMPLETE, Document
from core.methods import send_notifications


@task()
def process_document(document: Document):
    send_notifications(notification_type="notification", content="Processing document")
    uploaded_pdf = mistral.files.upload(
        file={
            "file_name": document.file.name,
            "content": open(f"media/{document.file.name}", "rb"),
        },
        purpose="ocr",
    )

    signed_url = mistral.files.get_signed_url(file_id=uploaded_pdf.id)

    ocr_response = mistral.ocr.process(
        model="mistral-ocr-latest",
        document={"type": "document_url", "document_url": signed_url.url},
        include_image_base64=False,
    )
    # print(ocr_response)

    content = ""

    for page in ocr_response.model_dump().get("pages", []):
        content += page["markdown"]
    # print(ocr_response.model_dump())

    send_notifications(notification_type="notification", content="Summarizing")
    pm = PromptManager(model="gpt-4.1")
    pm.add_messages(
        role="system",
        content="Please summarize the provided text. Extract also the key points"
        )
    pm.add_messages(
        role="system",
        content=f"Content: {content}"
    )

    summarized_content = pm.generate()

    document.raw_text = content
    document.summary = summarized_content
    document.status = DOC_STATUS_COMPLETE
    document.save()

    send_notifications(notification_type="notification", content="Creating document")

    splitter = SemanticChunker(OpenAIEmbeddings())
    documents = splitter.create_documents([content])

    collection = chroma.create_collection(name=document.id, embedding_function=openai_ef)
    collection.add(
        documents=[doc.model_dump().get("page_content") for doc in documents],
        ids=[str(i) for i in range(len(documents))]
    )

    send_notifications(notification_type="notification", content="Done")

    # print(json.dumps(documents, indent=2))