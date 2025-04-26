from uuid import UUID
from app.core.repositories.book_repository import BookRepository

class ReturnBookUseCase:
    def __init__(
        self,
        book_repo: BookRepository,
    ):
        self.book_repo = book_repo

    def execute(self, book_id: UUID) -> None:
        book = self.book_repo.get(book_id)
        if not book:
            raise ValueError("Book not found")

        book.return_book()
        self.book_repo.update(book)