import json
import math
import os
import re
from dotenv import load_dotenv
from openai import OpenAI
from typing import List, Tuple

from token_limits import TokenLimits


system_content_path = os.path.join(os.path.dirname(__file__), "data/system_content.json")
chatlog_path = os.path.join(os.path.dirname(__file__), "data/chatlog.json")


class CommentAnalyser:
    """ Analyse comments in source code. """
    def __init__(self):
        # Load OpenAI API key from environment variables
        load_dotenv()
        if os.getenv('OPENAI_API_KEY') is not None:
            self.api_key = os.getenv('OPENAI_API_KEY')
        else:
            raise ValueError(
                "OpenAI API key is not set in the environment variables.")
        
        # Load token limits for OpenAI models
        self.token_limits = TokenLimits()

    def analyse_comments(self, prompt: str, model: str = "gpt-4o-mini"
                         ) -> list:
        """ Analyse comments in source code. """
        chunks = self._split_prompt(prompt, model)
        suggestions = []
        for chunk in chunks:
            response = self._get_openai_response(chunk, model)
            suggestions.append(self._parse_openai_response(response))
        return suggestions

    def _split_prompt(self, prompt: str, model: str) -> List[str]:
        """ Split prompt into multiple chunks to avoid token limit. """
        chunk_size = math.ceil(
            self.token_limits.get_token_limit(model) * 0.75)
        chunks = []
        for i in range(0, len(prompt), chunk_size):
            chunks.append(prompt[i:i + chunk_size])
        return chunks

    def _get_openai_response(self, prompt: str, model: str) -> List[str]:
        """ Get response from OpenAI API. """
        with open(system_content_path, "r") as file:
            system_content = json.load(file).get("system_content")
        with open(chatlog_path, "r") as file:
            chatlog = json.load(file)
        messages = [
            {"role": "system", "content": system_content},
            *chatlog,
            {"role": "user", "content": prompt}
        ]
        client = OpenAI(api_key=self.api_key)
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.1,
            n=3,
            )
        print(f'completion tokens: {response.usage.completion_tokens}')
        print(f'prompt tokens: {response.usage.prompt_tokens}')
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
                f'OpenAI response is not in the expected format.\n{response}')

        return suggestions
