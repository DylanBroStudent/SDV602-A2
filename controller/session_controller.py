from data.session_repository import SessionRepository
from view.session_view       import SessionView

import FreeSimpleGUI as sg



def launch_session(session_id):
    controller = SessionController(session_id)
    controller.run()

class SessionController:
    def __init__(self, session_id):
        self.session_id = session_id
        self.repository = SessionRepository()
        self.session    = self.repository.get_one_by_id(session_id)
        self.view       = SessionView(self.session.name)


    def run(self):
        while True:
            event, values = self.view.read()

            if event in (sg.WIN_CLOSED, "-CLOSE-"):
                break

        self.view.close()
