from data.session_repository import SessionRepository
from data.database_manager   import DatabaseManager
from view.browser_view       import BrowserView

import FreeSimpleGUI as sg
import config


class SessionController:
    def __init__(self, user):
        self.user       = user
        self.username   = user.name
        self.repository = SessionRepository()
        self.view       = BrowserView()
        self.db         = DatabaseManager.getInstance()

    def run(self):
        sessions = self.repository.all()
        self.view.update_sessions(sessions)

        while True:
            event, values = self.view.read(timeout=config.POLL_RATE)

            if event == sg.WIN_CLOSED:
                break

            if event == "__TIMEOUT__":
                selected = values["-SESSION_TABLE-"]
                sessions = self.repository.all()
                
                self.view.update_sessions(sessions, selected)

            if event == "Create Session":
                name = sg.popup_get_text("Enter new session name:")
                SessionRepository.create_session(self.repository, self.username, name)
                sessions = self.repository.all()
                self.view.update_sessions(sessions)

            if event == "Join Session":
                pass

            if event == "Logout":
                pass

        self.view.close()