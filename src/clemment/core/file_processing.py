import os
from pathlib import Path
from typing import TypedDict, List, Tuple
from .openai_client_factory import OpenAIClientFactory
from .comment_analyser import CommentAnalyser
from ..utils.path_utils import discover_files


class CommentAnalysis(TypedDict):
    file_path: str
    suggestions: List[Tuple[int, str]]  # line_number, suggestion
    prompt_tokens: int
    completion_tokens: int


def process_file(path: str, comment_analyser: CommentAnalyser
                 ) -> CommentAnalysis:
    """
    Process a single file to analyze comments.

    Args:
        path (str): The path to the file to be processed.
    """
    with open(path, "r") as file:
        source_code = file.read()
    suggestions = comment_analyser.analyse_comments(source_code)
    return {
        "file_path": path,
        "suggestions": suggestions,
        "prompt_tokens": comment_analyser.total_prompt_tokens,
        "completion_tokens": comment_analyser.total_completion_tokens,
    }


def analyse_comments_in_path(
        path: Path,
        comment_analyser: CommentAnalyser = CommentAnalyser(
            OpenAIClientFactory().create_client())
            ) -> List[CommentAnalysis]:
    """
    Process a directory to analyze comments in all files.

    Args:
        path (str): The path to the directory to be processed.
    """
    if os.path.isfile(path):
        return [process_file(path, comment_analyser)]

    result = []
    for file_path in discover_files(path):
        result.append(process_file(file_path, comment_analyser))
    return result
