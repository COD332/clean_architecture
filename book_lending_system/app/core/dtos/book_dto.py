from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class BookDTO(BaseModel):
    id: UUID
    title: str
    author: str
    isbn: str
    borrower_id: Optional[UUID] = None

class CreateBookDTO(BaseModel):
    title: str
    author: str
    isbn: str
