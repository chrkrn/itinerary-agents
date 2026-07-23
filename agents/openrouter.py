import requests
import os
import json
from dotenv import load_dotenv
import logging
logger = logging.getLogger(__name__)

load_dotenv()

def chat_completion(messages, retry_count=3):
    """
    Call the OpenRouter API for chat completion
    """

    or_api_key = os.getenv("OPENROUTER_API_KEY")
    model = os.getenv("OPENROUTER_MODEL", "nvidia/nemotron-3-super-120b-a12b:free")

    logger.info(f"Calling OpenRouter API with model: {model}")

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {or_api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": model,
            "messages": messages
        }
    )

    logger.debug(f"OpenRouter API response status: {response.status_code}")

    response.raise_for_status()
    return response.json()