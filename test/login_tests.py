from data.database_manager import DatabaseManager
from data.user_repository  import UserRepository

from model.user import User

import config

class LoginTests:
    def __init__(self):
        self.db = DatabaseManager.getInstance()
        self.repository = UserRepository()

        # Unique username so future tests don't trip up
        import uuid
        self.username = f"test_{uuid.uuid4().hex[:12]}"
        self.password = "Admin123"

    def test_register_account(self):
        self.repository.create_user(self.username, self.password)

        stored_user = self.db.find_one_by_name(config.USER_COLLECTION, self.username)
        assert stored_user is not None

    def test_register_account_exists(self):
        stored_user = self.db.find_one_by_name(config.USER_COLLECTION, "TakenUsername")
        if stored_user is not None:
            self.repository.create_user("TakenUsername", self.password)

        user = self.repository.create_user("TakenUsername", self.password)
        assert user is None

    def test_login_incorrect_password(self):
        user = self.repository.login(self.username, "incorrect")
        assert user is None

    def test_login_correct_password(self):
        user = self.repository.login(self.username, self.password)
        assert isinstance(user, User)

    def test_login_unknown_user(self):
        user = self.repository.login("unknown", "incorrect")
        assert user is None