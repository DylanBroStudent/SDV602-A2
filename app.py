import argparse

from controller.login_controller   import LoginController
from controller.browser_controller import BrowserController

from data.user_repository    import UserRepository
from data.message_repository import MessageRepository

from test.test_manager import TestManager


class App:
    def __init__(self, headless = False):
        self.headless           = headless
        self.user_repository    = UserRepository()
        self.message_repository = MessageRepository()

    def run(self):
        login_controller = LoginController(self.user_repository)

        if self.headless:
            test_manager = TestManager()
            test_manager.run_all_tests()
            return
        else:
            # loop around to catch logouts
            while True:
                login_controller = LoginController(self.user_repository)
                user = login_controller.run()

                # if no user returned, crash the program
                if user is None:
                    break

                # catch the logout message
                outcome = BrowserController(user).run()
                # if any outcome besides logout, crash the program.
                if outcome != "logout":
                    break
            


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-headless",
        action = "store_true"
    )
    args = parser.parse_args()

    app = App(headless = args.headless)
    app.run()