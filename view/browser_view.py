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
                num_rows          = 10
            )],
            [
                sg.Button('Join Session'), 
                sg.Button('Create Session'), 
                sg.Exit('Logout')
            ]
        ]

        self.window = sg.Window("Session Browser", self.layout, finalize=True)

    def update_sessions(self, sessions):
        selected = values["-TABLE-"]
        formatted = self.format_sessions(sessions)
        self.window['-SESSION_TABLE-'].update(formatted)

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
        print("")
        if sessions:
            output = []
            for session in sessions:
                row = [
                    session.name,
                    session.host,
                    len(session.participants)
                ]
                output.append(row)
            return output