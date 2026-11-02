from data.database_manager   import DatabaseManager
from data.session_repository import SessionRepository

import config
import uuid


class SessionTests:
    def __init__(self):
        self.db         = DatabaseManager.get_test_instance()
        self.repository = SessionRepository(self.db)

        self.username     = f"test_{uuid.uuid4().hex[:12]}"

    def test_create_session(self):
        self.session_name = f"session_{uuid.uuid4().hex[:8]}"

        session_id = self.repository.create_session(
            self.username,
            self.session_name
        )

        stored_session = self.db.find_one_by_id(
            config.SESSION_COLLECTION,
            session_id
        )

        assert stored_session is not None

    def test_create_session_no_name(self):
        self.repository.create_session(self.username,"")

    def test_delete_session(self):
        session_id = self.repository.create_session(
            self.username,
            self.session_name
        )

        self.repository.delete_session(session_id)

        session = self.repository.get_one_by_id(session_id)

        assert session is None