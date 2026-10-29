from controller.session_controller import SessionController
from data.session_repository       import SessionRepository
from data.database_manager         import DatabaseManager
from view.browser_view             import BrowserView

from multiprocessing import Process

import FreeSimpleGUI as sg
import config


class BrowserController:
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

            if event == "-SESSION_TABLE-":
                # sessions = self.refresh_sessions(sessions, values)
                pass

            if event == "__TIMEOUT__":
                sessions = self.refresh_sessions(sessions, values)

            if event == "Create Session":

                name = sg.popup_get_text("Enter new session name:")

                # check name
                if name is None or not name.strip():
                    sg.popup_error("session name cannot be empty")
                    continue

                name = name.strip()
                
                SessionRepository.create_session(self.repository, self.username, name)
                
                sessions = self.repository.all()
                self.view.update_sessions(sessions)

            if event == "Join Session":
                selected_id = self.get_selected_session_id(sessions, values["-SESSION_TABLE-"])

                if selected_id is None:
                    sg.popup_error("Please select a session.")
                    continue

                self.join_session(selected_id)
                

            if event == "Logout":
                self.view.close()
                return "logout"
                
        self.view.close()
        

    
    def get_selected_session_id(self, sessions, selected_rows):
        
        # no row selected
        if not selected_rows:
            return None
        
        selected_row = selected_rows[0]

        return sessions[selected_row].id


    def refresh_sessions(self, sessions, values):

        selected = self.get_selected_session_id(sessions, values["-SESSION_TABLE-"])
        sessions = self.repository.all()

        self.view.update_sessions(sessions, selected)

        return sessions


    def join_session(self, session_id):
        process = Process(
            target = SessionController.launch,
            args   = (session_id,)
        )
        process.start()