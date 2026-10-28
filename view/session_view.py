import FreeSimpleGUI as sg

from matplotlib.figure                 import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class SessionView:
    def __init__(self, session_name):
        sg.theme("DarkBlue")
        
        self.session_name = session_name

        layout = [
            [sg.Text(f"Session: {session_name}", font=("Arial", 16, "bold"))],
            [
                sg.Button("Import CSV",    key="-IMPORT-CSV-"),
                sg.Button("Close Session", key="-CLOSE-"),
            ],
            [sg.HorizontalSeparator()],
            [sg.Canvas(key="-GRAPH-CANVAS-", size=(600, 400))],
        ]

        self.window = sg.Window(
            f"Session - {session_name}",
            layout,
            resizable=True,
            finalize=True,
        )

    def draw_graph(self, x_values, y_values, title="Data Graph", x_label="X", y_label="Y"):
        figure = Figure(figsize=(6, 4), dpi=100)
        axes   = figure.add_subplot(111)

        axes.plot(x_values, y_values, marker="o")
        axes.set_title(title)
        axes.set_xlabel(x_label)
        axes.set_ylabel(y_label)
        axes.grid(True)

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