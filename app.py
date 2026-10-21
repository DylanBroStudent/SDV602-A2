from data.user_repository    import UserRepository
from data.message_repository import MessageRepository
from model.user              import User

from controller.login_controller   import LoginController
from controller.session_controller import SessionController


HEADLESS = False

class App:
    def __init__(self):
        self.user_repository    = UserRepository()
        self.message_repository = MessageRepository()

    def run(self):
        login_controller = LoginController(self.user_repository)

        if HEADLESS:
            user = login_controller.login("a", "a")
            if type(user) == User:
                print("success")
        else:
            user = login_controller.run()

            if user:
                SessionController(user).run()
            else:
                print(user)


if __name__ == "__main__":
    app = App()
    app.run()