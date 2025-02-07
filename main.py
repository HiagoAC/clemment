import argparse
import os

from helpers import analyse_comments_in_path

def parse_arguments() -> argparse.Namespace:
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Run command
    run_parser = subparsers.add_parser("run", help="Analyse source code files")
    run_parser.add_argument(
        "paths", nargs="*", help="Paths to source code files.")

    # Chatlog commands
    chatlog_parser = subparsers.add_parser("chatlog", help="Chatlog commands")
    chatlog_subparsers = chatlog_parser.add_subparsers(dest="chatlog_command")

    add_chatlog_parser = chatlog_subparsers.add_parser("add", help="Add chatlog")
    chatlog_subparsers.add_parser("get", help="Get chatlog")
    chatlog_subparsers.add_parser("clear", help="Clear chatlog")

    add_chatlog_parser.add_argument(
        "-u", "--user", required=True, help="User input for chatlog.")
    add_chatlog_parser.add_argument(
        "-a", "--assistant", required=True, help="Assistant response for chatlog.")

    return parser.parse_args()

def main() -> None:
    """
    Main function to parse command line arguments and process files or
    directories.
    """
    args = parse_arguments()

    # Analyse comments in each path
    analysis_list = []
    total_prompt_tokens = 0
    total_completion_tokens = 0

    if args.command == "chatlog":
        pass
    elif args.command == "run":
        if args.paths:
            paths = args.paths
        else:
            paths = [os.getcwd()]
        for path in paths:
            if not os.path.exists(path):
                print(f"Invalid path: {path}")
                continue
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


if __name__ == "__main__":
    main()
