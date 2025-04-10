import os
from openai import OpenAI
from dotenv import load_dotenv


class OpenAIClientFactory:
    """ Factory class to create OpenAI client. """
    def create_client(self, api_key: str | None = None) -> OpenAI:
        if api_key is None:
            load_dotenv()
            if os.getenv('OPENAI_API_KEY') is not None:
                api_key = os.getenv('OPENAI_API_KEY')
            else:
                raise RuntimeError(
                    """
                    OPENAI_API_KEY is missing.
                    --> Get a key from https://platform.openai.com/api-keys
                    --> Then add it to a .env file:
                    --> OPENAI_API_KEY=your_key
                    """)
        return OpenAI(api_key=api_key)
