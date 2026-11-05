from data.database_manager import DatabaseManager
from datetime import datetime
import config

from model.chat_message import ChatMessage

class MessageRepository:
    def __init__(self, db = None):
        self.db = db if db is not None else DatabaseManager.getInstance()

    def create_message(self, session_id, username, text, timestamp=None):
        if timestamp is None:
            timestamp = datetime.now()

        return self.db.insert_one(config.CHAT_MESSAGES_COLLECTION, {
            "session_id": session_id,
            "username": username,
            "text": text,
            "timestamp": timestamp
        })


    def all(self, session_id):
        collection = self.db.get_collection(config.CHAT_MESSAGES_COLLECTION)

        messages = []

        for document in collection.find({"session_id": session_id}).sort("timestamp", 1):
            message = ChatMessage(
                document["username"],
                document["text"],
                document["timestamp"]
            )

            messages.append(message)

        return messages