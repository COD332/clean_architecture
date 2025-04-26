from typing import Dict, List, Optional
from uuid import UUID
from app.core.entities.book import Book
from app.core.entities.user import User
from app.core.repositories.book_repository import BookRepository
from app.core.repositories.user_repository import UserRepository
from app.core.dtos.pagination import PaginationParams, PaginatedResult

class InMemoryBookRepository(BookRepository):
    def __init__(self):
        self.storage: Dict[UUID, Book] = {}

    def add(self, book: Book) -> None:
        self.storage[book.id] = book

    def get(self, book_id: UUID) -> Optional[Book]:
        return self.storage.get(book_id)

    def list(self, params: PaginationParams) -> PaginatedResult[Book]:
        items = list(self.storage.values())
        total = len(items)
        start = (params.page - 1) * params.size
        end = start + params.size
        paginated_items = items[start:end]
        pages = (total + params.size - 1) // params.size
        return PaginatedResult(
            items=paginated_items,
            total=total,
            page=params.page,
            size=params.size,
            pages=pages
        )

    def update(self, book: Book) -> None:
        self.storage[book.id] = book

class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self.storage: Dict[UUID, User] = {}

    def add(self, user: User) -> None:
        self.storage[user.id] = user

    def get(self, user_id: UUID) -> Optional[User]:
        return self.storage.get(user_id)

    def list(self, params: PaginationParams) -> PaginatedResult[User]:
        items = list(self.storage.values())
        total = len(items)
        start = (params.page - 1) * params.size
        end = start + params.size
        paginated_items = items[start:end]
        pages = (total + params.size - 1) // params.size
        return PaginatedResult(
            items=paginated_items,
            total=total,
            page=params.page,
            size=params.size,
            pages=pages
        )

# **Single, shared instances**:
book_repo = InMemoryBookRepository()
user_repo = InMemoryUserRepository()
