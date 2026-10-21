class User:
    def __init__(self, name, password, password_hash=None):
            self.name          = name
            self.password_hash = password_hash