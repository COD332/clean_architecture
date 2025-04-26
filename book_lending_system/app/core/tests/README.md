# Core Tests for Book Lending System

This directory contains unit tests for the core functionality of the Book Lending System, which has been built using Clean Architecture principles. These tests are designed to validate the core business logic independently of any frameworks, databases, or external dependencies.

## Test Structure

The tests are organized into the following files:

- `test_mock_repositories.py`: Contains mock implementations of repositories for testing
- `test_user_operations.py`: Tests for user-related operations
- `test_book_operations.py`: Tests for book-related operations
- `test_lend_return_operations.py`: Tests for lending and returning books
- `run_tests.py`: Main test runner to execute all tests with a single command

## Test Coverage

The tests cover all primary operations of the system:

1. Adding users
2. Retrieving user information
3. Adding books
4. Retrieving book information
5. Lending books to users
6. Returning books
7. Error handling for all operations

## Running the Tests

To run all tests, simply execute the `run_tests.py` script from the command line:

```bash
python run_tests.py
```

Or you can make it executable and run it directly:

```bash
chmod +x run_tests.py
./run_tests.py
```

## Installation in Your Project

To install these tests in your project:

1. Create a directory `app/core/tests` if it doesn't already exist
2. Copy all the test files into this directory
3. Make sure you have the following project dependencies:
   - Python 3.6+
   - The core modules of your book lending system

## Notes

- These tests use Python's standard `unittest` framework and don't require any additional testing libraries
- The tests use mock repositories to isolate the core logic from any database dependencies
- All tests can be run without setting up any external infrastructure

## Test Output

The tests will output detailed results for each test case, showing success or failure. For each failure, the test will show the assertion error and the line number where the error occurred.

## Future Improvements

- Add more edge cases and negative tests
- Implement test fixtures for more complex scenarios
- Add code coverage reporting
- Add parameterized tests for common operations