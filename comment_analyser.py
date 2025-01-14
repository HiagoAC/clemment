import os
import re
from dotenv import load_dotenv
from openai import OpenAI
from typing import List, Tuple

from constants.chatlog import CHATLOG
from constants.system_content import SYSTEM_CONTENT


class CommentAnalyser:
    """ Analyse comments in source code. """
    def __init__(self):
        load_dotenv()
        if os.getenv('OPENAI_API_KEY') is not None:
            self.api_key = os.getenv('OPENAI_API_KEY')
        else:
            raise ValueError(
                "OpenAI API key is not set in the environment variables.")

    def analyse_comments(self, prompt: str, model: str = "gpt-4o-mini"
                         ) -> list:
        response = self._get_openai_response(prompt, model)
        suggestions = self._parse_openai_response(response)
        return suggestions

    def _get_openai_response(self, prompt: str, model: str) -> str:
        """ Get response from OpenAI API. """
        messages = [
            {"role": "system", "content": SYSTEM_CONTENT},
            *CHATLOG,
            {"role": "user", "content": prompt}
        ]
        client = OpenAI(api_key=self.api_key)
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.1,
            )
        print(f'model: {model}')
        print(f'completion tokens: {response.usage.completion_tokens}')
        print(f'prompt tokens: {response.usage.prompt_tokens}')
        # print(response.choices[0].message.content)
        return response.choices[0].message.content

    def _parse_openai_response(self, response: str) -> List[Tuple[int, str]]:
        """ Parse OpenAI response to the following format:
            [(line_number, suggestion), ...]
        """
        suggestions = []
        pattern = r"(\d+), (.+)"
        for line in response.split("\n"):
            match = re.match(pattern, line.strip())
            if match:
                line_number, suggestion = match.groups()
                suggestions.append((int(line_number), suggestion))
            else:
                raise ValueError(
                    f'OpenAI response is not in the expected format.
                    \n{response}')
        return suggestions