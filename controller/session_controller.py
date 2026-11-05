from data.session_repository import SessionRepository
from view.session_view       import SessionView

import config

import FreeSimpleGUI as sg
import csv
import os


def launch_session(session_id):
    controller = SessionController(session_id)
    controller.run()

class SessionController:
    def __init__(self, session_id, repository = None, create_view = True):
        self.session_id        = session_id
        self.repository        = repository if repository is not None else SessionRepository()
        self.session           = self.repository.get_one_by_id(session_id)
        self.previous_datasets = None

        self.view       = None
        
        # make session able to be initialised without a view for headless testing
        if create_view:
            self.view = SessionView(self.session.name)
            self.update_datasets()
            self.update_graph()


    def run(self):
        
        while True:
            event, values = self.view.read(timeout = config.POLL_RATE)

            if event == sg.TIMEOUT_EVENT:
                self.update_datasets()
                self.update_graph()
                continue

            if event == "-CSV_PATH-":
                file_path = values["-CSV_PATH-"]

                if file_path:
                    try:
                        self.import_csv(file_path)
                        self.update_datasets()

                    except ValueError as e:
                        sg.popup_error(str(e))

            if event == "-REMOVE_DATASET-":
                filename = values["-DATASET-"]

                if filename:
                    self.repository.remove_data(self.session_id, filename)
                    self.update_datasets()
            
            if event == "-SERIES-":
                selected_series = values["-SERIES-"]

                for dataset in self.session.data:
                    enabled_series = [
                        item.split(" : ", 1)[1]
                        for item in selected_series
                        if item.startswith(dataset["filename"] + " : ")
                    ]
                    
                    self.repository.update_enabled_series(
                        self.session_id,
                        dataset["filename"],
                        enabled_series
                    )

                self.update_graph()

            if event in (sg.WIN_CLOSED, "-CLOSE-"):
                break


        self.view.close()

    def import_csv(self, file_path):
        # open file
        with open(file_path, "r") as csv_file:
            # read file
            csv_reader = csv.DictReader(csv_file)

            data = []

            for row in csv_reader:
                data.append(row)

        self.session = self.repository.get_one_by_id(self.session_id)

        # prevent duplicate files
        for existing_dataset in self.session.data:
            if existing_dataset["filename"] == os.path.basename(file_path):
                raise ValueError("Dataset already imported")
            
        dataset = {
            "filename"      : os.path.basename(file_path),
            "columns"       : csv_reader.fieldnames,
            "enabled_series": [],
            "rows"          : data
        }

        # add to repository
        self.repository.add_data(self.session_id, dataset)

        # Debug
        # print("CSV imported successfully:", dataset["filename"])
        # print("Columns:", dataset["columns"])
        # print("Rows imported:", len(dataset["rows"]))


    def update_datasets(self):
        self.session     = self.repository.get_one_by_id(self.session_id)
        
        selected_dataset = self.view.window["-DATASET-"].get()
        selected_series  = self.view.window["-SERIES-" ].get()
        x_axis           = self.view.window["-X_AXIS-" ].get()
        y_axis           = self.view.window["-Y_AXIS-" ].get()

        datasets       = []
        series         = []
        columns        = []

        for dataset in self.session.data:
            filename = dataset["filename"]
            datasets.append(filename)

            for column in dataset["columns"]:
                series.append(f"{filename} : {column}")

                if column not in columns:
                    columns.append(column)

        first_load = self.previous_datasets is None
        if first_load:
            selected_series = []

            for dataset in self.session.data:
                for column in dataset.get("enabled_series", []):
                    selected_series.append(f'{dataset["filename"]} : {column}')

        current_datasets = (datasets, columns, series)

        if self.previous_datasets != current_datasets:
            self.view.update_datasets(datasets, columns, series)
            self.previous_datasets = current_datasets
        
        # update the selected dataset
        if selected_dataset in datasets:
            self.view.window["-DATASET-"].update(value=selected_dataset)
        elif datasets:
            self.view.window["-DATASET-"].update(value=datasets[0])

        # update series select box
        selected_indices = []

        for item in selected_series:
            if item in series:
                selected_indices.append(series.index(item))

        self.view.window["-SERIES-"].update(
            set_to_index = selected_indices
)

        # update the axes
        if x_axis in columns:
            self.view.window["-X_AXIS-"].update(value = x_axis)
        elif columns:
            self.view.window["-X_AXIS-"].update(value = columns[0])

        if y_axis in columns:
            self.view.window["-Y_AXIS-"].update(value = y_axis)
        elif columns:
            self.view.window["-Y_AXIS-"].update(value = columns[1] if len(columns) > 1 else columns[0])


    def update_series(self, filename):
        self.session = self.repository.get_one_by_id(self.session_id)

        for dataset in self.session.data:
            if dataset["filename"] == filename:
                enabled_series = dataset.get("enabled_series", [])

                self.view.window["-SERIES-"].update(
                    values       = dataset["columns"],
                    set_to_index = [
                        dataset["columns"].index(series)
                        for series in enabled_series
                        if series in dataset["columns"]
                    ]
                )

                break


    def update_graph(self):
        # get data
        graph_data = self.get_graph_data()

        # validate
        if graph_data is None:
            return
        
        # get values
        x_values, series = graph_data

        # draw the graph
        self.view.draw_graph(
            x_values,
            series,
            x_label=self.view.window["-X_AXIS-"].get(),
            title=self.session.name
        )


    def get_graph_data(self):
        self.session = self.repository.get_one_by_id(self.session_id)

        x_key           = self.view.window["-X_AXIS-"].get()
        selected_series = self.view.window["-SERIES-"].get()

        if not x_key or not selected_series:
            return None

        series   = {} # Dictionary
        x_values = [] # List

        for selected in selected_series:
            filename, column = selected.split(" : ", 1)

            for dataset in self.session.data:
                if dataset["filename"] == filename:
                    series[selected] = {}

                    for row in dataset["rows"]:
                        x_value = row[x_key]
                        y_value = float(row[column])

                        series[selected][x_value] = y_value

                        if x_value not in x_values:
                            x_values.append(x_value)

                    break

        x_values.sort()

        graph_series = {}

        for name, data in series.items():
            graph_series[name] = [
                data.get(x, None) for x in x_values
            ]

        return x_values, graph_series