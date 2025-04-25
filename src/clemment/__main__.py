from .core.comment_analyser import CommentAnalyser
from .core.clients import create_openai_client
from .cli import parse_arguments, run, chatlog
from .config import SYSTEM_CONTENT_PATH, CHATLOG_PATH


def main() -> None:
    """
    Main function to parse command line arguments and process files or
    directories.
    """
    args = parse_arguments()

    if args.command == "chatlog":
        chatlog(args)
    elif args.command == "run":
        comment_analyser = CommentAnalyser(
            client=create_openai_client(),
            system_content_path=SYSTEM_CONTENT_PATH,
            chatlog_path=CHATLOG_PATH
        )
        run(args, comment_analyser)


if __name__ == "__main__":
    main()
