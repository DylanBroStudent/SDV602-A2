import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

DB_NAME                  = "session_23"
DATA_SOURCES_COLLECTION  = "data_sources"
CHAT_MESSAGES_COLLECTION = "chat_messages"
SESSION_COLLECTION       = "sessions"
USER_COLLECTION          = 'users'

POLL_RATE=1000