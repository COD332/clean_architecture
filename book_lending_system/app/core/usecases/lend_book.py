from uuid import UUID
from app.core.repositories.book_repository import BookRepository
from app.core.repositories.user_repository import UserRepository

class LendBookUseCase:
    def __init__(
        self,
        book_repo: BookRepository,
        user_repo: UserRepository,
    ):
        self.book_repo = book_repo
        self.user_repo = user_repo

    def execute(self, book_id: UUID, user_id: UUID) -> None:
        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError("User not found")

        book = self.book_repo.get(book_id)
        if not book:
            raise ValueError("Book not found")

        book.lend_to(user.id)
        self.book_repo.update(book)