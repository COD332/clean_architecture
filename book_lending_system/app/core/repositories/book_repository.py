from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from app.core.entities.book import Book
from app.core.dtos.pagination import PaginationParams, PaginatedResult

class BookRepository(ABC):

    @abstractmethod
    def add(self, book: Book) -> None:
        pass

    @abstractmethod
    def get(self, book_id: UUID) -> Optional[Book]:
        pass

    @abstractmethod
    def list(self, pagination: PaginationParams) -> PaginatedResult[Book]:
        pass

    @abstractmethod
    def update(self, book: Book) -> None:
        pass