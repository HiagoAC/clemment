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

    def _get_openai_response(self, prompt: str, model: str) -> List[str]:
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
            n=3,
            )
        print(f'model: {model}')
        print(f'completion tokens: {response.usage.completion_tokens}')
        print(f'prompt tokens: {response.usage.prompt_tokens}')
        # print(response.choices[0].message.content)
        return [choice.message.content for choice in response.choices]

    def _parse_openai_response(self, responses: List[str]) -> List[Tuple[int, str]]:
        """ Parse OpenAI response to the following format:
            [(line_number, suggestion), ...]
        """
        suggestions = []
        pattern = r"(\d+), (.+)"
        for response in responses:
            for line in response.split("\n"):
                match = re.match(pattern, line.strip())
                if match:
                    line_number, suggestion = match.groups()
                    suggestions.append((int(line_number), suggestion))
                else: 
                # If the response is not in the expected format,
                # try the next response
                    suggestions = []
                    break
            # If the response is in the expected format, ignore next responses
            break
            
        if not suggestions:
            raise ValueError(
                f'OpenAI response is not in the expected format.
                \n{response}')

        return suggestions