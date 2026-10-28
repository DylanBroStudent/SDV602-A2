from view.session_view import SessionView

import FreeSimpleGUI as sg


class SessionController:
    def __init__(self, session_name):
        self.session_name = session_name
        self.view         = SessionView(session_name)

    def run(self):
        while True:
            event, values = self.view.read()

            if event in (sg.WIN_CLOSED, "-CLOSE-"):
                break

        self.view.close()
