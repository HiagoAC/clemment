import os
from dotenv import load_dotenv

from .utils.path_utils import get_absolute_path


# CONSTANTS

CHATLOG_PATH = get_absolute_path('chatlog.json', ['data'])
SYSTEM_CONTENT_PATH = get_absolute_path('system_content.json', ['data'])

MODEL_TOKEN_LIMITS = {
    "gpt-4": 8192,
    "gpt-4-turbo": 128000,
    "gpt-4o": 128000,
    "gpt-4o-mini": 128000,
    "o1": 200000,
    "o1-mini": 128000,
}


# CONFIG HELPER FUNCTIONS

def get_openai_api_key() -> str:
    """Get OpenAI API key from environment variable or .env file."""
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key is None:
        raise RuntimeError(
            """
            OPENAI_API_KEY is missing.
            --> Get a key from https://platform.openai.com/api-keys
            --> Then add it to a .env file:
            --> OPENAI_API_KEY=your_key
            """)
    return api_key
