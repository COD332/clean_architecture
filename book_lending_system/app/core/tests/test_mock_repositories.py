"""
Mock repositories for testing purposes
"""
import sys
import os
from typing import Dict, List, Optional
from uuid import UUID

# Add project root directory to path to allow importing modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from app.core.entities.user import User
from app.core.entities.book import Book
from app.core.repositories.user_repository import UserRepository
from app.core.repositories.book_repository import BookRepository
from app.core.dtos.pagination import PaginationParams, PaginatedResult

class MockUserRepository(UserRepository):
    def __init__(self):
        self.users: Dict[UUID, User] = {}
    
    def add(self, user: User) -> None:
        self.users[user.id] = user
    
    def get(self, user_id: UUID) -> Optional[User]:
        return self.users.get(user_id)
    
    def list(self) -> List[User]:
        return list(self.users.values())
    
    def clear(self) -> None:
        """Clear all users - for testing purposes"""
        self.users.clear()


class MockBookRepository(BookRepository):
    def __init__(self):
        self.books: Dict[UUID, Book] = {}
    
    def add(self, book: Book) -> None:
        self.books[book.id] = book
    
    def get(self, book_id: UUID) -> Optional[Book]:
        return self.books.get(book_id)
    
    def list(self, pagination: PaginationParams) -> PaginatedResult[Book]:
        all_books = list(self.books.values())
        
        # Calculate pagination
        start_idx = (pagination.page - 1) * pagination.size
        end_idx = start_idx + pagination.size
        items = all_books[start_idx:end_idx]
        
        total_items = len(all_books)
        total_pages = (total_items + pagination.size - 1) // pagination.size
        
        return PaginatedResult(
            items=items,
            total=total_items,
            page=pagination.page,
            size=pagination.size,
            pages=total_pages
        )
    
    def update(self, book: Book) -> None:
        self.books[book.id] = book
    
    def clear(self) -> None:
        """Clear all books - for testing purposes"""
        self.books.clear()