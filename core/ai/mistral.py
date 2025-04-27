import os

from mistralai import Mistral

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

client = Mistral(api_key=MISTRAL_API_KEY)
