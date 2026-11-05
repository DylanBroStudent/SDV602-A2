from view.chat_view import ChatView

import config
import FreeSimpleGUI as sg


class ChatController:
    def __init__(self, session_id, username, message_repository, view):
        self.session_id         = session_id
        self.username           = username
        self.message_repository = message_repository
        self.view               = view


    def update_messages(self):
        messages = self.message_repository.all(self.session_id)
        self.view.update_messages(messages)


    def send_message(self, text):
        if text:
            self.message_repository.create_message(
                self.session_id,
                self.username,
                text
            )

            self.view.clear_chat_input()
            self.update_messages()