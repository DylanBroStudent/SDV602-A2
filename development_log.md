### Development Log

## Index
1. Login and Registration
2. Headless testing
3. Session Browser
4. Session Window



# 1. Login and Registration

login and registration were built as part of classwork. I followed the tutors guidance and built a basic login and registration screen as part of their lessons.
A chat sytem was also prototyped, but it is unfinished and will later be implemented in the session window.

# 2. Headless Testing

Using argpass I've implemented the tag -headless, which switches the main app logic to run a suite of tests against the program.

I've built a useful and very nicely formatted function to run each test, compare the outcome against an expected outcome, and print the results. The expected outcome may be an error, and so if it fails correctly, its considered a pass. likewise, a successful outcome when an error was expected is considered a fail.

I chose a middle-ground approach to comparing the outcomes. I didn't want to compare whether it produced an exception or not since it may produce the wrong type of exception. And I also didn't want to compare specific exception messages as that gets far too complicated. Instead I compare the type of exception such as ValueError or TypeError. Which is close enough and keeps things simple.

Each area of testing has its own _tests.py file such as login_tests which hold the logic for each test in accessible functions for the test_manager.py to pass into the testing function.


# 3. Session Browser

The session browser is essentially a table of all the active sessions in the database. It uses much of the same logic as the prototype chat system to constantly refresh itself.

I encountered an issue with the refresh logic as it would lose the currently selected item in the table, making it difficult to select one and join before it was deselected.
At first I used the index of the selected row, but realised that in the event of the list changing, if sessions were created or deleted, the selected session may jump to a new row. So I overhauled the refresh logic to save and pass on the id of the selected row, so once the table is refreshed, it can reselect that specific session.

Ensuring the table can only have one selected row at a time made things a lot more stable.

I wanted to refresh the table whenever a new row was selected, but unfortunately that results in an infinite loop as the refresh ends by reselecting the row, causing the refresh to trigger again. I've disabled the behavior for now and may revisit in a later iteration.

the logout button was tricky to impliment as it required overhauling the app.py logic. I've encased the top level app logic in a loop, that will return to the login screen in the event of the session browser closing.

