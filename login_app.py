import FreeSimpleGUI as sg

from view.login_view import LoginView
from view.register_view import RegisterView
from model.user import User


def register():
    view = RegisterView()

    while True:
        event, values = view.read()

        if event in (sg.WIN_CLOSED, "Cancel", "Login"):
            view.close()
            return

        if event == "Register":
            try:
                User(values["-USERNAME-"], values["-PASSWORD-"]).save()
                view.show_message("Registration successful")
                view.close()
                return
            except Exception as e:
                view.show_error(e)


def login():
    view = LoginView()

    while True:
        event, values = view.read()

        if event in (sg.WIN_CLOSED, "Cancel"):
            view.close()
            return

        if event == "Register":
            view.close()
            register()
            view = LoginView()

        if event == "Login":
            if User.login(values["-USERNAME-"], values["-PASSWORD-"]):
                view.show_message("Login successful")
                view.close()
                return

            view.show_error("Login failed")


if __name__ == "__main__":
    login()