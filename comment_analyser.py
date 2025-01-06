import os
from dotenv import load_dotenv
from openai import OpenAI


class CommentAnalyser:
    """ Analyse comments in source code. """
    def __init__(self):
        load_dotenv()
        if os.getenv('OPENAI_API_KEY') is not None:
            self.api_key = os.getenv('OPENAI_API_KEY')
        else:
            raise ValueError(
                "OpenAI API key is not set in the environment variables.")
