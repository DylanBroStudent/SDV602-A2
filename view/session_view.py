
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure                 import Figure

import FreeSimpleGUI as sg

class SessionView:
    def __init__(self, session_name):
        sg.theme("DarkBlue")

        self.session_name = session_name

        layout = [
            [
                sg.Text(
                    f"Session: {self.session_name}",
                    font=("Arial", 16, "bold"),
                    expand_x=True
                ),
                sg.Button("Close Session", key="-CLOSE-")
            ],
            [
                # LEFT COLUMN
                sg.Column([
                    [sg.Canvas(
                        key="-GRAPH-CANVAS-",
                        size=(650, 400),
                        expand_x=True,
                        expand_y=True
                    )],
                    [sg.HorizontalSeparator()],
                    [sg.Text("Graph Controls", font=("Arial", 12, "bold"))],
                    [
                        sg.Button("Import CSV", key="-IMPORT-CSV-")
                    ],
                    [
                        sg.Text("Graph Title"),
                        sg.Input(key="-TITLE-", expand_x=True)
                    ],
                    [
                        sg.Text("X Axis"),
                        sg.Input(key="-X-LABEL-", expand_x=True)
                    ],
                    [
                        sg.Text("Y Axis"),
                        sg.Input(key="-Y-LABEL-", expand_x=True)
                    ]
                ], expand_x=True, expand_y=True),

                # RIGHT COLUMN
                sg.Column([
                    [sg.Text("Session Chat", font=("Arial", 12, "bold"))],
                    [
                        sg.Multiline(
                            size=(35, 25),
                            key="-CHAT-HISTORY-",
                            disabled=True,
                            expand_x=True,
                            expand_y=True
                        )
                    ],
                    [
                        sg.Input(
                            key="-CHAT-INPUT-",
                            expand_x=True
                        ),
                        sg.Button("Send", key="-SEND-CHAT-")
                    ]
                ], expand_x=True, expand_y=True)
            ]
        ]

        self.window = sg.Window(
            f"Session - {self.session_name}",
            layout,
            resizable=True,
            finalize=True,
        )

    def draw_graph(self, x_values, y_values, title="Data Graph", x_label="X", y_label="Y"):
        figure = Figure(figsize=(6, 4), dpi=100)
        axes   = figure.add_subplot(111)

        axes.plot      (x_values, y_values, marker="o")
        axes.set_title (title)
        axes.set_xlabel(x_label)
        axes.set_ylabel(y_label)
        axes.grid      (True)

        self.graph_canvas = FigureCanvasTkAgg(
            figure,
            master=self.window["-GRAPH-CANVAS-"].TKCanvas,
        )
        self.graph_canvas.draw()
        self.graph_canvas.get_tk_widget().pack(
            side   = "top",
            fill   = "both",
            expand = True,
    )

    def read(self, timeout=None):
        return self.window.read(timeout=timeout)

    def close(self):
        self.window.close()