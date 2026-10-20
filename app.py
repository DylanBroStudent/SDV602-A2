# import os
# import subprocess
# import sys

import FreeSimpleGUI as sg

# Multiprocessing alternative imports:
import multiprocessing
from chat_app import run as run_chat


def run():
    layout = [
        [sg.Button("Open Chat"), sg.Button("Exit")],
    ]
    window = sg.Window("Chat Launcher", layout)
    active_chats = []

    while True:
        event, values = window.read(timeout=1000)

        if event in (sg.WIN_CLOSED, "Exit"):
            break

        if event == "Open Chat":
            # app_folder = os.path.dirname(os.path.abspath(__file__))

            # Each chat runs independently in a new Python process.
            # process = subprocess.Popen(
            #     [sys.executable, os.path.join(app_folder, "chat_app.py")],
            #     cwd=app_folder,
            # )

            # Multiprocessing replacement for subprocess.Popen:
            process = multiprocessing.Process(target=run_chat)
            process.start()

            active_chats.append(process)

        # Remove processes from the list when their chat window has closed.
        for process in list(active_chats):
            # if process.poll() is not None:
            #     active_chats.remove(process)

            # Multiprocessing replacement for process.poll():
            if not process.is_alive():
                active_chats.remove(process)

    # process.terminate() works for subprocess and multiprocessing.
    for process in active_chats:
        process.terminate()

    window.close()


if __name__ == "__main__":
    run()