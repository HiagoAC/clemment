import argparse
import os

from helpers import analyse_comments_in_path
from openai_client_factory import OpenAIClientFactory

def main() -> None:
    """
    Main function to parse command line arguments and process files or
    directories.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", help="Paths to source code files.")
    args = parser.parse_args()

    analysis_list = []
    total_prompt_tokens = 0
    total_completion_tokens = 0

    for path in args.paths:
        if not os.path.exists(path):
            print(f"Invalid path: {path}")
            continue
        responses = analyse_comments_in_path(path)
        for res in responses:
            analysis_list.append((res["file_path"], res["suggestions"]))
            total_prompt_tokens += res["prompt_tokens"]
            total_completion_tokens += res["completion_tokens"]

    print(f"Total prompt tokens: {total_prompt_tokens}")
    print(f"Total completion tokens: {total_completion_tokens}")
    print("Suggestions:")
    for path, suggestions in analysis_list:
        print(f"File: {path}")
        for line_number, suggestion in suggestions:
            print(f"Line {line_number}: {suggestion}")


if __name__ == "__main__":
    main()
