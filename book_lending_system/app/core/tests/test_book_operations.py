"""
Tests for book-related core operations
"""
import unittest
import sys
import os
from uuid import uuid4

# Add project root directory to path to allow importing modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from app.core.entities.book import Book
from app.core.dtos.pagination import PaginationParams
from app.core.tests.test_mock_repositories import MockBookRepository

class TestBookOperations(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.book_repo = MockBookRepository()
    
    def tearDown(self):
        """Tear down test fixtures after each test method"""
        self.book_repo.clear()
    
    def test_add_book(self):
        """Test adding a book to the repository"""
        # Arrange
        book = Book(
            title="Clean Architecture",
            author="Robert C. Martin",
            isbn="9780134494166"
        )
        
        # Act
        self.book_repo.add(book)
        
        # Assert
        retrieved_book = self.book_repo.get(book.id)
        self.assertIsNotNone(retrieved_book)
        self.assertEqual(retrieved_book.title, "Clean Architecture")
        self.assertEqual(retrieved_book.author, "Robert C. Martin")
        self.assertEqual(retrieved_book.isbn, "9780134494166")
        self.assertEqual(retrieved_book.id, book.id)
    
    def test_get_book(self):
        """Test retrieving a book from the repository"""
        # Arrange
        book = Book(
            title="Domain-Driven Design",
            author="Eric Evans",
            isbn="9780321125217"
        )
        self.book_repo.add(book)
        
        # Act
        retrieved_book = self.book_repo.get(book.id)
        
        # Assert
        self.assertIsNotNone(retrieved_book)
        self.assertEqual(retrieved_book.title, "Domain-Driven Design")
        self.assertEqual(retrieved_book.author, "Eric Evans")
    
    def test_get_nonexistent_book(self):
        """Test retrieving a non-existent book"""
        # Act
        retrieved_book = self.book_repo.get(uuid4())
        
        # Assert
        self.assertIsNone(retrieved_book)
    
    def test_list_books_with_pagination(self):
        """Test listing books with pagination"""
        # Arrange
        for i in range(25):
            book = Book(
                title=f"Book {i+1}",
                author=f"Author {i+1}",
                isbn=f"ISBN-{i+1}"
            )
            self.book_repo.add(book)
        
        # Act - Page 1 (default 20 per page)
        pagination = PaginationParams(page=1, size=10)
        result = self.book_repo.list(pagination)
        
        # Assert
        self.assertEqual(len(result.items), 10)
        self.assertEqual(result.total, 25)
        self.assertEqual(result.page, 1)
        self.assertEqual(result.size, 10)
        self.assertEqual(result.pages, 3)
        
        # Act - Page 2
        pagination = PaginationParams(page=2, size=10)
        result = self.book_repo.list(pagination)
        
        # Assert
        self.assertEqual(len(result.items), 10)