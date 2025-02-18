from cli import parse_arguments, run, chatlog


def main() -> None:
    """
    Main function to parse command line arguments and process files or
    directories.
    """
    args = parse_arguments()

    if args.command == "chatlog":
        chatlog(args)
    elif args.command == "run":
        run(args)


if __name__ == "__main__":
    main()
