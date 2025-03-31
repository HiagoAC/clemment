import os
import argparse

from clemment.core.file_processing import analyse_comments_in_path


def run(args: argparse.Namespace) -> None:
    """
    Analyse source code files in the given paths and output suggestions.
    """
    analysis_list = []
    total_prompt_tokens = 0
    total_completion_tokens = 0
    if args.paths:
        paths = args.paths
    else:
        paths = [os.getcwd()]
    for path in paths:
        if not os.path.exists(path):
            raise ValueError(f"Invalid path: {path}")
        responses = analyse_comments_in_path(path)
        for res in responses:
            analysis_list.append((res["file_path"], res["suggestions"]))
            total_prompt_tokens += res["prompt_tokens"]
            total_completion_tokens += res["completion_tokens"]

    # Output analysis results
    print(f"Total prompt tokens: {total_prompt_tokens}")
    print(f"Total completion tokens: {total_completion_tokens}")
    print("Suggestions:")
    for path, suggestions in analysis_list:
        print(f"File: {path}")
        for line_number, suggestion in suggestions:
            print(f"Line {line_number}: {suggestion}")
