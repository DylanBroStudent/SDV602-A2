from data.database_manager import DatabaseManager
import bcrypt
import config


class User:

    db = DatabaseManager.getInstance()

    def __init__(self, name, password):
        # self.id = id
        self.name = name

        try:
            password_encoded = password.encode("utf-8")
            # hash password with bcrypt
            salt = bcrypt.gensalt()
            password_hash = bcrypt.hashpw(password_encoded, salt)

            self.password_hash = password_hash
        except Exception as e:
            print(f"Something went wrong: {e}")


        self.db = DatabaseManager.getInstance()

    @classmethod
    def login(cls, username, password):    
        if not type(password) == str or not password:
            raise Exception("Invalid Password")

        try:
            # get user by name
            stored_user = cls.db.find_one_by_name(config.USER_COLLECTION, username)
            if not stored_user:
                raise Exception("Failed to find user")
            
            # compare pw
            password_encoded = password.encode("utf-8")
            # print(stored_user["password"])
            result = bcrypt.checkpw(password_encoded, stored_user["password"])

            if not result:
                raise Exception("Failed to login: Incorrect Password")

            # create and return user
            return cls(username, password)
        except Exception as e:
            print(f"Something went wrong: {e}")
    
    def save(self):
        if self.db.find_one_by_name(config.USER_COLLECTION, self.name):
            raise Exception("Username already taken")
        
        return self.db.insert_one(config.USER_COLLECTION, {
            "name": self.name,
            "password": self.password_hash
        })