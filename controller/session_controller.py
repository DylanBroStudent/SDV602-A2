from data.session_repository import SessionRepository
from view.browser_view       import BrowserView

import FreeSimpleGUI as sg
import config


class SessionController:
    def __init__(self, user):
        self.user       = user
        self.repository = SessionRepository()
        self.view       = BrowserView()

    def run(self):
        sessions = self.repository.all()
        self.view.update_sessions(sessions)

        while True:
            event, values = self.view.read(timeout=config.POLL_RATE)

            if event == sg.WIN_CLOSED:
                break

            if event == "__TIMEOUT__":
                sessions = self.repository.all()
                self.view.update_sessions(sessions)

            if event == "Create Session":
                pass

            if event == "Join Session":
                pass

            if event == "Logout":
                pass

        self.view.close()