from data.database_manager         import DatabaseManager
from data.session_repository       import SessionRepository
from controller.session_controller import SessionController

import config
import uuid


class ImportTests:
    def __init__(self):
        self.db         = DatabaseManager.get_test_instance()
        self.repository = SessionRepository(self.db)

        self.username     = f"test_       {uuid.uuid4().hex[:12]}"
        self.session_name = f"import_test_{uuid.uuid4().hex[:8]}"

        self.session_id = self.repository.create_session(
            self.username,
            self.session_name
        )

    def test_import_csv(self):
        controller = SessionController(
            self.session_id,
            repository  = self.repository,
            create_view = False
        )

        controller.import_csv("test/files/test_data_01.csv")

        session = self.repository.get_one_by_id(self.session_id)

        assert session.data[0]["filename"]  == "test_data_01.csv"


    def test_import_duplicate_csv(self):
        controller = SessionController(
            self.session_id,
            repository  = self.repository,
            create_view = False
        )

        controller.import_csv("test/files/test_data_01.csv")


    def test_remove_dataset(self):
        session = self.repository.get_one_by_id(self.session_id)

        self.repository.remove_data(self.session_id, "test_data_01.csv")

        session = self.repository.get_one_by_id(self.session_id)

        assert len(session.data) == 0