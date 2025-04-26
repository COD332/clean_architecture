"""
Main test runner for book lending system core tests
"""
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from app.core.tests.test_user_operations import TestUserOperations
from app.core.tests.test_book_operations import TestBookOperations
from app.core.tests.test_lend_return_operations import TestLendReturnOperations

if __name__ == '__main__':
    loader = unittest.TestLoader()
    test_suite = unittest.TestSuite()

    test_suite.addTests(loader.loadTestsFromTestCase(TestUserOperations))
    test_suite.addTests(loader.loadTestsFromTestCase(TestBookOperations))
    test_suite.addTests(loader.loadTestsFromTestCase(TestLendReturnOperations))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    sys.exit(not result.wasSuccessful())
