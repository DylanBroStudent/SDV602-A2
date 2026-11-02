
from data.database_manager import DatabaseManager


class DatabaseTests:
    def __init__(self):
        self.db = DatabaseManager.get_test_instance()

    def test_connection(self):
        result = self.db.client.admin.command("ping")
        assert result.get("ok") == 1.0