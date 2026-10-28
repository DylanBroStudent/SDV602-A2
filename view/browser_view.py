import FreeSimpleGUI as sg


class BrowserView:

    def __init__(self):
        sg.theme("DarkBlue")

        self.layout = [
            [sg.Text("Session Browser", font=("Helvetica", 14))],
            [sg.Table(
                values            = [],
                headings          = ["Session Name", "Host", "Active Users"],
                auto_size_columns = False,
                col_widths        = [25, 15, 10],
                key               = '-SESSION_TABLE-',
                enable_events     = True,
                num_rows          = 10,
                select_mode       = sg.TABLE_SELECT_MODE_BROWSE
            )],
            [
                sg.Button('Join Session'),
                sg.Button('Create Session'),
                sg.Exit('Logout')
            ]
        ]

        self.window = sg.Window("Session Browser", self.layout, finalize=True)

    def update_sessions(self, sessions, selected = None):
        formatted = self.format_sessions(sessions)
        
        selected_rows = []
        if selected is not None:
            for i, session in enumerate(sessions):
                if session.id == selected:
                    selected_rows.append(i)
        
        self.window['-SESSION_TABLE-'].update(
            values      = formatted, 
            select_rows = selected_rows or []
        )

    def clear_input(self):
        self.window['-SEARCH-'].update('')

    def read(self, timeout=None):
        return self.window.read(timeout=timeout)

    def close(self):
        self.window.close()

    def show_error(self, session):
        sg.popup_error(session)

    def show_session(self, session):
        sg.popup(session)

    def format_sessions(self, sessions=[]):
        if sessions is None:
            sessions = []

        output = []
        for session in sessions:
            row = [
                session.name,
                session.host,
                len(session.participants)
            ]
            output.append(row)
        return output