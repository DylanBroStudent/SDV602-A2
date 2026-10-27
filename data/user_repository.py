from data.database_manager import DatabaseManager
import bcrypt
import config

from model.user import User

class UserRepository:
    def __init__(self):
        self.db = DatabaseManager.getInstance()
        

    def login(self, username, password):    
        if not type(password) == str or not password:
            raise ValueError("Invalid Password")

        try:
            # get user by name
            stored_user = self.db.find_one_by_name(config.USER_COLLECTION, username)
            
            if not stored_user:
                raise ValueError("User not found")
            
            # compare pw
            password_encoded = password.encode("utf-8")
            # print(stored_user["password"])
            result = bcrypt.checkpw(password_encoded, stored_user["password"])

            if not result:
                raise ValueError("Incorrect Password")

            # create and return user
            return User(username, password)

        except ValueError:
            # Catch all value errors
            raise
        except Exception as e:
            # Catch everything else
            print(f"Something went wrong: {e}")

    
    def create_user(self, username, password):
        
        # check for existing user
        if self.db.find_one_by_name(config.USER_COLLECTION, username):
            raise ValueError("Username already taken")

        password_hash = None
        try:
            password_encoded = password.encode("utf-8")
            # hash password with bcrypt
            salt = bcrypt.gensalt()
            password_hash = bcrypt.hashpw(password_encoded, salt)
        except Exception as e:
            print(f"Something went wrong: {e}")

        
        return self.db.insert_one(config.USER_COLLECTION, {
            "name": username,
            "password": password_hash
        })


