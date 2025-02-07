import json


class ChatLogManager:
    """ Class to manage chatlog data """

    def __init__(self, path="data/chatlog.json"):
        self.path = path
        with open(self.path, "r") as file:
            self.chatlog = json.load(file)

    def add_chatlog(self, user_input, assistant_response):
        """ Add chatlog to chatlog list. """
        self.chatlog.append({"role": "user", "content": user_input})
        self.chatlog.append({"role": "assistant", "content": assistant_response})

    def get_chatlog(self):
        return self.chatlog

    def clear_chatlog(self):
        """ Clear all data in chatlog. """
        self.chatlog.clear()

    def save_chatlog(self):
        with open(self.path, "w") as file:
            json.dump(self.chatlog, file)
