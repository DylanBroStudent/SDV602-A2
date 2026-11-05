from data.database_manager import DatabaseManager
from model.session         import Session

import config


class SessionRepository:
    def __init__(self, db = None):
        self.db = db if db is not None else DatabaseManager.getInstance()


    def create_session(self, host, name):

        if not name or not name.strip():
            raise ValueError("Session name cannot be empty")
        
        return self.db.insert_one(config.SESSION_COLLECTION, {
            "host"         : host,
            "name"         : name,
            "status"       : "active",
            "participants" : [],
            "data"         : []
        })
    
    def delete_session(self, session_id):
        collection = self.db.get_collection(config.SESSION_COLLECTION)
        collection.delete_one({"_id": session_id})

    def remove_data(self, session_id, filename):
        collection = self.db.get_collection(config.SESSION_COLLECTION)

        collection.update_one(
            {"_id": session_id},
            {"$pull": {"data": {"filename": filename}}}
        )
    
    def get_one_by_id(self, session_id):
        collection = self.db.get_collection(config.SESSION_COLLECTION)
        document   = collection.find_one({"_id": session_id})

        if document is None:
            return None

        return Session(
            session_id   = document["_id"],
            name         = document["name"],
            host         = document["host"],
            status       = document["status"],
            participants = document["participants"],
            data         = document.get("data", [])
        )


    def all(self):
        collection = self.db.get_collection(config.SESSION_COLLECTION)
        sessions   = []

        for document in collection.find({"status": "active"}).sort("name"):
            
            session = Session(
                session_id   = document["_id"],
                name         = document["name"], 
                host         = document["host"], 
                status       = document["status"],
                participants = document["participants"],
                data         = document.get("data", [])
            )
            sessions.append(session)
        return sessions


    def add_data(self, session_id, dataset):
        collection = self.db.get_collection(config.SESSION_COLLECTION)

        collection.update_one(
            {"_id"  : session_id},
            {"$push": {"data": dataset}}
        )

    def update_enabled_series(self, session_id, filename, enabled_series):
        collection = self.db.get_collection(config.SESSION_COLLECTION)

        collection.update_one(
            {"_id" : session_id, "data.filename": filename},
            {"$set": {"data.$.enabled_series": enabled_series}}
        )