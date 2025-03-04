import os
from openai import OpenAI
from dotenv import load_dotenv

class OpenAIClientFactory:
    """ Factory class to create OpenAI client. """
    def create_client(self, api_key: str | None = None) -> OpenAI:
        if api_key is None:
            # Load OpenAI API key from environment variables
            load_dotenv()
            if os.getenv('OPENAI_API_KEY') is not None:
                api_key = os.getenv('OPENAI_API_KEY')
            else:
                raise ValueError(
                    "OpenAI API key is not set in the environment variables.")
        return OpenAI(api_key=api_key)
