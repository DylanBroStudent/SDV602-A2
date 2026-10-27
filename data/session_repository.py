from data.database_manager import DatabaseManager
from model.session         import Session

import config


class SessionRepository:
    def __init__(self):
        self.db = DatabaseManager.getInstance()

    def create_session(self, host, name):
        
        return self.db.insert_one(config.SESSION_COLLECTION, {
            "host"         : host,
            "name"         : name,
            "status"       : "active",
            "participants" : [host]
        })


    def all(self):
        collection = self.db.get_collection(config.SESSION_COLLECTION)
        sessions = []

        for document in collection.find({"status": "active"}).sort("name"):
            
            session = Session(
                session_id   = document["_id"],
                name         = document["name"], 
                host         = document["host"], 
                status       = document["status"],
                participants = document["participants"]
            )
            
            sessions.append(session)

        return sessions