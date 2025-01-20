import argparse
import os
from typing import TypedDict, List, Tuple

from comment_analyser import CommentAnalyser

class ProcessFileResult(TypedDict):
    suggestions: List[Tuple[int, str]]
    prompt_tokens: int
    completion_tokens: int


def main() -> None:
    """
    Main function to parse command line arguments and process files or
    directories.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", help="Paths to source code files.")
    args = parser.parse_args()

    suggestions = []
    total_prompt_tokens = 0
    total_completion_tokens = 0

    for path in args.paths:
        if os.path.isfile(path):
            res = process_file(path)
            suggestions.append((path, res["suggestions"]))
            total_prompt_tokens += res["prompt_tokens"]
            total_completion_tokens += res["completion_tokens"]
        elif os.path.isdir(path):
            process_directory(path)
        else:
            print(f"Invalid path: {path}")

    print(f"Total prompt tokens: {total_prompt_tokens}")
    print(f"Total completion tokens: {total_completion_tokens}")
    print("Suggestions:")
    for path, suggestion in suggestions:
        print(f"File: {path}")
        for line_number, suggestion in suggestions:
            print(f"Line {line_number}: {suggestion}")


def process_file(path: str) -> ProcessFileResult:
    """
    Process a single file to analyze comments.

    Args:
        path (str): The path to the file to be processed.
    """
    with open(path, "r") as file:
        source_code = file.read()

    comment_analyser = CommentAnalyser()
    suggestions = comment_analyser.analyse_comments(source_code)
    
    return {
        "suggestions": suggestions,
        "prompt_tokens": comment_analyser.total_prompt_tokens,
        "completion_tokens": comment_analyser.total_completion_tokens,
    }


def process_directory(path: str) -> None:
    """
    Process a directory to analyze comments in all files.

    Args:
        path (str): The path to the directory to be processed.
    """
    for _, _, files in os.walk(path):
        for file in files:
            process_file(os.path.join(path, file))


if __name__ == "__main__":
    main()
