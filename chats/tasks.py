from huey.contrib.djhuey import task

from core.ai.chromadb import chroma, openai_ef
from core.ai.prompt_manager import PromptManager
from core.methods import send_chat_message

import json


SYSTEM_PROMPT_RAG = """
You are a helpful asisstant,
Your task is to answer the question based on the document.

PROVIDED DOCUMENTS:
{documents}

ANSWER GUIDELINES:
- Always answer in Bahasa Indonesia
- Do not include any additional information other than provided document

"""

@task()
def process_chat(message, document_id):

    collection = chroma.get_collection(document_id, embedding_function=openai_ef)
    res = collection.query(query_texts=[message], n_results=3)

    pm = PromptManager()
    pm.add_messages("system", SYSTEM_PROMPT_RAG.format(documents=json.dumps(res)))
    pm.add_messages("user", message)

    assistant_messages = pm.generate()
    send_chat_message(assistant_messages)
