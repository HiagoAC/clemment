from openai import OpenAI
from src.clemment.config import get_openai_api_key


def create_openai_client() -> OpenAI:
    api_key = get_openai_api_key()
    return OpenAI(api_key=api_key)
