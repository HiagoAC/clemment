import argparse


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

    add_chatlog_parser = chatlog_subparsers.add_parser(
        "add", help="Add chatlog")
    chatlog_subparsers.add_parser("get", help="Get chatlog")
    chatlog_subparsers.add_parser("clear", help="Clear chatlog")

    add_chatlog_parser.add_argument(
        "-u", "--user", required=True, help="User input for chatlog.")
    add_chatlog_parser.add_argument(
        "-a",
        "--assistant",
        required=True,
        help="Assistant response for chatlog."
    )

    return parser.parse_args()
