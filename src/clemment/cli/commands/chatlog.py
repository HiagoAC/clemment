import argparse
from ...core.chatlog_manager import ChatLogManager


def chatlog(args: argparse.Namespace) -> None:
    """
    Process chatlog commands.
    """
    chatlog_manager = ChatLogManager()
    if args.chatlog_command == "add":
        chatlog_manager.add_chatlog(args.user, args.assistant)
        print("Chatlog added.")
    elif args.chatlog_command == "get":
        chatlog = chatlog_manager.get_chatlog()
        for log in chatlog:
            print(f"{log['role']}: {log['content']}")
    elif args.chatlog_command == "clear":
        chatlog_manager.clear_chatlog()
        print("Chatlog cleared.")
    chatlog_manager.save_chatlog()
