from data.session_repository import SessionRepository
from view.session_view       import SessionView

import FreeSimpleGUI as sg
import csv
import os


def launch_session(session_id):
    controller = SessionController(session_id)
    controller.run()

class SessionController:
    def __init__(self, session_id, repository = None, create_view = True):
        self.session_id = session_id
        self.repository = repository if repository is not None else SessionRepository()
        self.session    = self.repository.get_one_by_id(session_id)
        
        self.view       = None
        
        # make session able to be initialised without a view for headless testing
        if create_view:
            self.view = SessionView(self.session.name)
            self.update_datasets()


    def run(self):
        
        while True:
            event, values = self.view.read()

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
            "filename": os.path.basename(file_path),
            "columns" : csv_reader.fieldnames,
            "rows"    : data
        }

        # add to repository
        self.repository.add_data(self.session_id, dataset)
        



        # Debug
        # print("CSV imported successfully:", dataset["filename"])
        # print("Columns:", dataset["columns"])
        # print("Rows imported:", len(dataset["rows"]))

    def update_datasets(self):
        self.session = self.repository.get_one_by_id(self.session_id)

        datasets = [
            dataset["filename"]
            for dataset in self.session.data
        ]

        columns = (
            self.session.data[0]["columns"]
            if self.session.data else []
        )

        self.view.update_datasets(datasets, columns)

        if datasets:
            self.view.window["-DATASET-"].update(
                value=datasets[0]
            )