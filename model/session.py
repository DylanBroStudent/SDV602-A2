class Session:
    def __init__(
            self, 
            name, 
            host, 
            status       ="active", 
            participants = None, 
            session_id   = None,
            data         = None
            ):
        
        self.id           = session_id
        self.name         = name
        self.host         = host
        self.status       = status
        self.participants = participants if participants is not None else []
        self.data         = data         if data         is not None else []
        