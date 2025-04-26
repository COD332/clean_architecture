from typing import Optional
from uuid import UUID, uuid4

class Book:
    def __init__(
        self,
        title: str,
        author: str,
        isbn: str,
        id: Optional[UUID] = None,
        borrower_id: Optional[UUID] = None,
    ):
        self.id: UUID = id or uuid4()
        self.title = title
        self.author = author
        self.isbn = isbn
        self.borrower_id: Optional[UUID] = borrower_id

    def lend_to(self, user_id: UUID):
        if self.borrower_id:
            raise ValueError("Book is already lent out")
        self.borrower_id = user_id

    def return_book(self):
        if not self.borrower_id:
            raise ValueError("Book is not lent")
        self.borrower_id = None
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "borrower_id": str(self.borrower_id) if self.borrower_id else None,
        }
    
    def from_dict(data):
        return Book(
            title=data["title"],
            author=data["author"],
            isbn=data["isbn"],
            id=UUID(data["id"]),
            borrower_id=UUID(data["borrower_id"]) if data["borrower_id"] else None,
        )