from view.session_view import SessionView

import FreeSimpleGUI as sg



def launch_session(session_id):
    controller = SessionController(session_id)
    controller.run()

class SessionController:
    def __init__(self, session_id):
        self.session_id = session_id
        self.view       = SessionView(session_id)

    def run(self):
        while True:
            event, values = self.view.read()

            if event in (sg.WIN_CLOSED, "-CLOSE-"):
                break

        self.view.close()
