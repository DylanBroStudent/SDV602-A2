from test.database_tests import DatabaseTests
from test.login_tests    import LoginTests
from test.session_tests  import SessionTests
from test.import_tests   import ImportTests
from test.chat_tests     import ChatTests


class TestManager:
    def __init__(self):
        self.database_tests = DatabaseTests()
        self.login_tests    = LoginTests()
        self.session_tests  = SessionTests()
        self.import_tests   = ImportTests()
        self.chat_tests     = ChatTests()

        self.testing_tests = [
            ("Expected Success",   self.test_success,        None),
            ("Unexpected Success", self.test_success,        ValueError),
            ("Expected error",     self.test_expected_error, ValueError),
            ("Unexpected error",   self.test_expected_error, None),
            ("Wrong error",        self.test_wrong_error,    ValueError)
        ]
        self.database_tests = [
            ("Database connection", self.database_tests.test_connection, None)
        ]
        self.login_tests = [
            ("Register account",   self.login_tests.test_register_account,         None),
            ("Account exists",     self.login_tests.test_register_account_exists,  ValueError),
            ("Incorrect password", self.login_tests.test_login_incorrect_password, ValueError),
            ("Correct password",   self.login_tests.test_login_correct_password,   None),
            ("Unknown username",   self.login_tests.test_login_unknown_user,       ValueError)
        ]
        self.session_tests = [
            ("Create session",       self.session_tests.test_create_session,         None),
            ("Session with no name", self.session_tests.test_create_session_no_name, ValueError),
            ("Delete session",       self.session_tests.test_delete_session,         None)
        ]
        self.import_tests = [
            ("Import CSV",           self.import_tests.test_import_csv,           None),
            ("Import duplicate CSV", self.import_tests.test_import_duplicate_csv, ValueError),
            ("Remove Dataset",       self.import_tests.test_remove_dataset,       None)
        ]
        self.chat_tests = [
            ("Send message",       self.chat_tests.test_send_message,  None)
        ]


    def run_test(self, test_function, expected_outcome):
        
        if expected_outcome is None:    
            
            # test should succeed
            try:
                test_function()
                # test succeeded when it should have succeeded
                return "PASS", None
            
            except Exception as e:
                # test failed when it should have succeeded
                return "FAIL", f"{type(e).__name__}: {e}"
            
        else:

            # test should raise exception                    
            try:
                test_function()
                # test succeeded when it should have failed
                return "FAIL", None
            
            except expected_outcome as e:
                # test failed when it should have failed
                return "PASS", f"{type(e).__name__}: {e}"
            
            except Exception as e:
                # test failed in a different way than it should have failed
                return "FAIL", f"{type(e).__name__}: {e}"


    def run_all_tests(self):
        total_run    = 0
        total_passed = 0
        total_failed = 0

        print("\n1. TESTING TESTS")
        testing_test_results = self.run_tests(self.testing_tests)

        print("\n2. DATABASE TESTS")
        database_test_results = self.run_tests(self.database_tests)

        print("\n3. LOGIN TESTS")
        login_test_results = self.run_tests(self.login_tests)

        print("\n4. SESSION TESTS")
        session_test_results = self.run_tests(self.session_tests)

        print("\n5. IMPORT TESTS")
        import_test_results = self.run_tests(self.import_tests)

        print("\n6. CHAT TESTS")
        chat_test_results = self.run_tests(self.chat_tests)

        # Calculate totals
        total_run = (
            testing_test_results[0] +
            database_test_results[0] +
            login_test_results[0] +
            session_test_results[0] +
            import_test_results[0] +
            chat_test_results[0]
        )

        total_passed = (
            testing_test_results[1] +
            database_test_results[1] +
            login_test_results[1] +
            session_test_results[1] +
            import_test_results[1] +
            chat_test_results[1]
        )

        total_failed = (
            testing_test_results[2] +
            database_test_results[2] +
            login_test_results[2] +
            session_test_results[2] +
            import_test_results[2] +
            chat_test_results[2]
        )

        print("\nTEST SUMMARY")
        
        print(
            f"\n{'Category':<15}" 
            f"{'Run':>8}" 
            f"{'Passed':>10}" 
            f"{'Failed':>10}"
        )

        print("-------------------------------------------")

        print(
            f"{'Testing':<15}"
            f"{testing_test_results[0]:>8}"
            f"{testing_test_results[1]:>10}"
            f"{testing_test_results[2]:>10}"
        )

        print(
            f"{'Database':<15}"
            f"{database_test_results[0]:>8}"
            f"{database_test_results[1]:>10}"
            f"{database_test_results[2]:>10}"
        )

        print(
            f"{'Login':<15}"
            f"{login_test_results[0]:>8}"
            f"{login_test_results[1]:>10}"
            f"{login_test_results[2]:>10}"
        )

        print(
            f"{'Session':<15}"
            f"{session_test_results[0]:>8}"
            f"{session_test_results[1]:>10}"
            f"{session_test_results[2]:>10}"
        )

        print(
            f"{'Import':<15}"
            f"{import_test_results[0]:>8}"
            f"{import_test_results[1]:>10}"
            f"{import_test_results[2]:>10}"
        )

        print(
            f"{'Import':<15}"
            f"{chat_test_results[0]:>8}"
            f"{chat_test_results[1]:>10}"
            f"{chat_test_results[2]:>10}"
        )

        print("-------------------------------------------")

        print(
            f"{'TOTAL':<15}"
            f"{total_run:>8}"
            f"{total_passed:>10}"
            f"{total_failed:>10}"
        )



    def run_tests(self, test_list):
        tests_run    = 0
        tests_passed = 0
        tests_failed = 0

        for test in test_list:
            result, given_exception = self.run_test(test[1], test[2])
            tests_run += 1

            if result == "PASS":
                tests_passed += 1
                print(f"    Test: {test[0]:<25} Result:\033[92m {result:<10}\033[0m Expected: {str(test[2]):<25} Caught: {str(given_exception):<15}")

            else:
                tests_failed += 1
                print(f"    Test: {test[0]:<25} Result:\033[91m {result:<10}\033[0m Expected: {str(test[2]):<25} Caught: {str(given_exception):<15}")

        return tests_run, tests_passed, tests_failed

    
    def test_success(self):
        assert 1 + 1 == 2

    def test_expected_error(self):
        raise ValueError("Expected error")
    
    def test_wrong_error(self):
        raise TypeError("Wrong error")


if __name__ == "__main__":
    manager = TestManager()
    manager.run_all_tests()