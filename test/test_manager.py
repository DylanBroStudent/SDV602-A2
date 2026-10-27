from test.database_tests import DatabaseTests
from test.login_tests    import LoginTests

class TestManager:
    def __init__(self):
        self.database_tests = DatabaseTests()
        self.login_tests    = LoginTests()

        self.test_list = [
            # testing tests
            ("Expected Success", self.test_success,        None),
            ("Expected error",   self.test_expected_error, ValueError),
            ("Wrong error",      self.test_wrong_error,    ValueError),

            # database tests
            ("Database connection", self.database_tests.test_connection, None),

            # login tests
            ("Register account",   self.login_tests.test_register_account,         None),
            ("Incorrect password", self.login_tests.test_login_incorrect_password, ValueError),
            ("Correct password",   self.login_tests.test_login_correct_password,   None),
            ("Unknown username",   self.login_tests.test_login_unknown_user,       ValueError)
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
        tests_run    = 0
        tests_passed = 0
        tests_failed = 0

        for test in self.test_list:
            result, given_exception = self.run_test(test[1], test[2])
            tests_run += 1

            # proud of this formatting
            if result == "PASS":
                tests_passed += 1
                print(f"Test: {test[0]:<25} Result:\033[92m {result:<10}\033[0m Expected: {str(test[2]):<25} Caught: {str(given_exception):<15}")
                
            else:
                tests_failed += 1
                print(f"Test: {test[0]:<25} Result:\033[91m {result:<10}\033[0m Expected: {str(test[2]):<25} Caught: {str(given_exception):<15}")
                
        print(f"\nTests Run:    {tests_run} \nTests Passed: {tests_passed} \nTests Failed: {tests_failed}")

            
    def test_success(self):
        assert 1 + 1 == 2

    def test_expected_error(self):
        raise ValueError("Expected error")
    
    def test_wrong_error(self):
        raise TypeError("Wrong error")


if __name__ == "__main__":
    manager = TestManager()
    manager.run_all_tests()