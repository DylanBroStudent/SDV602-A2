class Session:
    def __init__(self, name, host, status="active", participants=None, session_id=None):
        self.id     = session_id
        self.name   = name
        self.host   = host
        self.status = status
        if (participants is not None):
            self.participants = participants
        else:
            self.participants = []