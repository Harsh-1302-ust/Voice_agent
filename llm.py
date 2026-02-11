from openai import AzureOpenAI
from config import (
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_VERSION,
    AZURE_DEPLOYMENT
)

client = AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_version=AZURE_OPENAI_API_VERSION,
)

SYSTEM_PROMPT = """
You're an expert voice agent. You are given the transcript of what
the user has said using voice. You need to output as if you are a
voice agent and whatever you speak will be converted back to audio.
"""

def ask_llm(history, web_context):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "system", "content": f"Web context:\n{web_context}"},
        *history
    ]

    response = client.chat.completions.create(
        model=AZURE_DEPLOYMENT,
        messages=messages
    )

    return response.choices[0].message.content
