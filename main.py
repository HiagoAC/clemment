import argparse
import os
from comment_analyser import CommentAnalyser


def main() -> None:
    """
    Main function to parse command line arguments and process files or
    directories.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", help="Paths to source code files.")

    # Parse command line arguments
    args = parser.parse_args()

    for path in args.paths:
        if os.path.isfile(path):
            process_file(path)
        elif os.path.isdir(path):
            process_directory(path)
        else:
            print(f"Invalid path: {path}")


def process_file(path: str) -> None:
    """
    Process a single file to analyze comments.

    Args:
        path (str): The path to the file to be processed.
    """
    with open(path, "r") as file:
        source_code = file.read()

    comment_analyser = CommentAnalyser()
    suggestions = comment_analyser.analyse_comments(source_code)

    print(f"File: {path}")
    for line_number, suggestion in suggestions:
        print(f"Line {line_number}: {suggestion}")


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
