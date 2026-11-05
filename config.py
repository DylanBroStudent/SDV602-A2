import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

DB_NAME                  = "session_26"
TEST_DB_NAME             = "session_26_test"
DATA_SOURCES_COLLECTION  = "data_sources"
CHAT_MESSAGES_COLLECTION = "chat_messages"
SESSION_COLLECTION       = "sessions"
USER_COLLECTION          = 'users'

POLL_RATE=1000