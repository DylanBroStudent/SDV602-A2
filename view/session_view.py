
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
                    font     = ("Arial", 16, "bold"),
                    expand_x = True
                ),
                sg.Button("Close Session", key="-CLOSE-")
            ],
            [
                # LEFT COLUMN
                sg.Column([
                    [sg.Canvas(
                        key      = "-GRAPH_CANVAS-",
                        size     = (650, 400),
                        expand_x = True,
                        expand_y = True
                    )],
                    [sg.HorizontalSeparator()],
                    [sg.Text("Graph Controls", font = ("Arial", 12, "bold"))],
                    [
                        sg.FileBrowse(
                            "Import CSV",
                            key        = "-IMPORT_CSV-",
                            target     = "-CSV_PATH-",
                            file_types = (("CSV Files", "*.csv"),)
                        ),
                        # invisible element to hold the path
                        sg.Input(
                            key           = "-CSV_PATH-",
                            visible       = False,
                            enable_events = True
                        )
                    ],
                    [
                        sg.Text("Dataset"),
                        sg.Combo(
                            values        = [],
                            key           = "-DATASET-",
                            expand_x      = True,
                            enable_events = True,
                            readonly      = True
                        ),
                        sg.Button("Remove", key="-REMOVE_DATASET-")
                    ],
                    [
                        sg.Text("X Axis"),
                        sg.Combo(
                            values        = [],
                            key           = "-X_AXIS-",
                            expand_x      = True,
                            enable_events = True,
                            readonly      = True
                        )
                    ],
                    [
                        sg.Text("Y Axis"),
                        sg.Combo(
                            values        = [],
                            key           = "-Y_AXIS-",
                            expand_x      = True,
                            enable_events = True,
                            readonly      = True
                        )
                    ],
                    [
                        sg.Text("Series"),
                        sg.Listbox(
                            values        = [],
                            key           = "-SERIES-",
                            select_mode   = sg.LISTBOX_SELECT_MODE_MULTIPLE,
                            size          = (20, 5),
                            expand_x      = True,
                            enable_events = True
                        )
                    ]
                ], expand_x = True, expand_y = True),

                # RIGHT COLUMN
                sg.Column([
                    [sg.Text("Session Chat", font = ("Arial", 12, "bold"))],
                    [
                        sg.Multiline(
                            size     = (35, 25),
                            key      = "-CHAT_HISTORY-",
                            disabled = True,
                            expand_x = True,
                            expand_y = True
                        )
                    ],
                    [
                        sg.Input(
                            key      = "-CHAT_INPUT-",
                            expand_x = True,
                            size     = (10, 1)
                        ),
                        sg.Button("Send", key = "-SEND_CHAT-")
                    ]
                ], expand_x = True, expand_y = True)
            ]
        ]

        self.window = sg.Window(
            f"Session - {self.session_name}",
            layout,
            resizable = True,
            finalize  = True,
            size      = (1280, 720),
        )
        # set minimum size
        self.window.TKroot.minsize(1000, 700)

    def draw_graph(self, x_values, series, x_label="X", title="Data Graph"):

        # create graph only once
        if not hasattr(self, "graph_canvas"):
            figure = Figure(figsize=(6, 4), dpi=100)
            self.axes = figure.add_subplot(111)

            self.graph_canvas = FigureCanvasTkAgg(
                figure,
                master=self.window["-GRAPH_CANVAS-"].TKCanvas
            )

            self.graph_canvas.get_tk_widget().pack(
                side="top",
                fill="both",
                expand=True
            )

        # clear previous data
        self.axes.clear()

        # draw updated data
        for name, y_values in series.items():
            self.axes.plot(x_values, y_values, marker="o", label=name)

        if series:
            self.axes.legend()

        self.axes.set_title(title)
        self.axes.set_xlabel(x_label)
        self.axes.grid(True)

        self.graph_canvas.draw_idle()

    
    def update_datasets(self, datasets, columns, series):
        self.window["-DATASET-"].update(values = datasets)
        self.window["-X_AXIS-" ].update(values = columns)
        self.window["-Y_AXIS-" ].update(values = columns)
        self.window["-SERIES-" ].update(values = series) 


    def read(self, timeout=None):
        return self.window.read(timeout=timeout)


    def close(self):
        self.window.close()