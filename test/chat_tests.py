
from data.database_manager   import DatabaseManager
from data.message_repository import MessageRepository
from data.session_repository import SessionRepository
import uuid


class ChatTests:
    def __init__(self):
        self.db = DatabaseManager.get_test_instance()

        self.message_repository = MessageRepository(self.db)
        self.session_repository = SessionRepository(self.db)

        self.username = f"test_{uuid.uuid4().hex[:8]}"

        self.session_id = self.session_repository.create_session(
            self.username,
            "chat_test"
        )

    def test_send_message(self):
        self.message_repository.create_message(
            self.session_id,
            self.username,
            "Hello world!"
        )

        messages = self.message_repository.all(self.session_id)

        assert messages[0].text == "Hello world!"

    def test_empty_message(self):
        messages_before = self.message_repository.all(self.session_id)

        self.message_repository.create_message(
            self.session_id,
            self.username,
            ""
        )

        messages_after = self.message_repository.all(self.session_id)

        assert len(messages_after) == len(messages_before)