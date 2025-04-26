"""
Tests for lending and returning book operations
"""
import unittest
import sys
import os
from uuid import uuid4

# Add project root directory to path to allow importing modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from app.core.entities.user import User
from app.core.entities.book import Book
from app.core.usecases.lend_book import LendBookUseCase
from app.core.usecases.return_book import ReturnBookUseCase
from app.core.tests.test_mock_repositories import MockUserRepository, MockBookRepository

class TestLendReturnOperations(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.user_repo = MockUserRepository()
        self.book_repo = MockBookRepository()
        
        # Create use cases
        self.lend_book_use_case = LendBookUseCase(
            book_repo=self.book_repo,
            user_repo=self.user_repo
        )
        
        self.return_book_use_case = ReturnBookUseCase(
            book_repo=self.book_repo
        )
        
        # Create test user and book
        self.user = User(name="Test User")
        self.user_repo.add(self.user)
        
        self.book = Book(
            title="Test Book",
            author="Test Author",
            isbn="TEST-ISBN-123"
        )
        self.book_repo.add(self.book)
    
    def tearDown(self):
        """Tear down test fixtures after each test method"""
        self.user_repo.clear()
        self.book_repo.clear()
    
    def test_lend_book_success(self):
        """Test successfully lending a book to a user"""
        # Act
        self.lend_book_use_case.execute(self.book.id, self.user.id)
        
        # Assert
        updated_book = self.book_repo.get(self.book.id)
        self.assertEqual(updated_book.borrower_id, self.user.id)
    
    def test_lend_book_nonexistent_book(self):
        """Test lending a non-existent book"""
        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.lend_book_use_case.execute(uuid4(), self.user.id)
        
        self.assertIn("Book not found", str(context.exception))
    
    def test_lend_book_nonexistent_user(self):
        """Test lending a book to a non-existent user"""
        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.lend_book_use_case.execute(self.book.id, uuid4())
        
        self.assertIn("User not found", str(context.exception))
    
    def test_lend_book_already_borrowed(self):
        """Test lending a book that is already borrowed"""
        # Arrange
        another_user = User(name="Another User")
        self.user_repo.add(another_user)
        
        # First lending
        self.lend_book_use_case.execute(self.book.id, self.user.id)
        
        # Act & Assert - Second lending attempt
        with self.assertRaises(ValueError) as context:
            self.lend_book_use_case.execute(self.book.id, another_user.id)
        
        self.assertIn("Book is already lent out", str(context.exception))
    
    def test_return_book_success(self):
        """Test successfully returning a book"""
        # Arrange - First lend the book
        self.lend_book_use_case.execute(self.book.id, self.user.id)
        
        # Act - Then return it
        self.return_book_use_case.execute(self.book.id)
        
        # Assert
        updated_book = self.book_repo.get(self.book.id)
        self.assertIsNone(updated_book.borrower_id)
    
    def test_return_book_nonexistent_book(self):
        """Test returning a non-existent book"""
        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.return_book_use_case.execute(uuid4())
        
        self.assertIn("Book not found", str(context.exception))
    
    def test_return_book_not_borrowed(self):
        """Test returning a book that isn't borrowed"""
        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.return_book_use_case.execute(self.book.id)
        
        self.assertIn("Book is not lent", str(context.exception))