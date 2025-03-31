import json
import math
import re
from openai import OpenAI
from typing import List, Tuple

from ..utils.path_utils import get_absolute_path
from .token_limits import TokenLimits


class CommentAnalyser:
    """ Analyse comments in source code. """
    def __init__(self, client: OpenAI):
        self.SYSTEM_CONTENT_PATH = get_absolute_path(
            'system_content.json', ['data'])
        self.CHATLOG_PATH = get_absolute_path(
            'chatlog.json', ['data'])
        self.total_completion_tokens = 0
        self.total_prompt_tokens = 0
        self.client = client

        # Load token limits for OpenAI models
        self.token_limits = TokenLimits()

    def analyse_comments(self, prompt: str, model: str = "gpt-4o-mini"
                         ) -> list:
        """ Analyse comments in source code. """
        chunks = self._split_prompt(prompt, model)
        suggestions = []
        for chunk in chunks:
            response = self._get_openai_response(chunk, model)
            suggestions.extend(self._parse_openai_response(response))
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
        with open(self.SYSTEM_CONTENT_PATH, "r") as file:
            system_content = json.load(file).get("system_content")
        with open(self.CHATLOG_PATH, "r") as file:
            chatlog = json.load(file)
        messages = [
            {"role": "system", "content": system_content},
            *chatlog,
            {"role": "user", "content": prompt}
        ]
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.1,
            n=3,
            )

        self.total_completion_tokens += response.usage.completion_tokens
        self.total_prompt_tokens += response.usage.prompt_tokens

        return [choice.message.content for choice in response.choices]

    def _parse_openai_response(self, responses: List[str]
                               ) -> List[Tuple[int, str]]:
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
            if suggestions:
                break

        if not suggestions:
            raise ValueError(
                f'OpenAI response is not in the expected format.\n{responses}')

        return suggestions
