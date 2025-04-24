from .core.comment_analyser import CommentAnalyser
from .core.clients import create_openai_client
from .cli import parse_arguments, run, chatlog


def main() -> None:
    """
    Main function to parse command line arguments and process files or
    directories.
    """
    args = parse_arguments()

    if args.command == "chatlog":
        chatlog(args)
    elif args.command == "run":
        comment_analyser = CommentAnalyser(create_openai_client())
        run(args, comment_analyser)


if __name__ == "__main__":
    main()
