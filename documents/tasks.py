from huey.contrib.djhuey import task
from documents.models import Document, DOC_STATUS_COMPLETE
from core.ai.mistral import mistral
from core.ai.prompt_manager import PromptManager


@task()
def process_document(document: Document):
    uploaded_pdf = mistral.files.upload(
        file={
            "file_name": document.file.name,
            "content": open(f"media/{document.file.name}", "rb"),
        },
        purpose="ocr",
    )

    signed_url = mistral.files.get_signed_url(file_id=uploaded_pdf.id)

    ocr_result = mistral.ocr.process(
        model="mistral-ocr-latest",
        document={"type": "document_url", "document_url": signed_url.url},
    )

    content = ""

    for page in ocr_result.model_dump().get("pages", []):
        content += page("markdown")

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