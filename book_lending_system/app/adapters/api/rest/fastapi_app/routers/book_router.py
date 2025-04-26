from fastapi import APIRouter, HTTPException, Depends
from typing import List
from uuid import UUID

from app.core.entities.book import Book
from app.adapters.db.repositories import book_repo, user_repo
from app.core.usecases.lend_book import LendBookUseCase
from app.core.usecases.return_book import ReturnBookUseCase
from app.core.dtos.book_dto import BookDTO, CreateBookDTO
from app.core.dtos.pagination import PaginationParams, PaginatedResult

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/", response_model=PaginatedResult[BookDTO])
def list_books(pagination: PaginationParams = Depends(PaginationParams)):
    """
    List all books with pagination.
    """
    books = book_repo.list(pagination)
    total_count = len(books.items)
    dto_items = [BookDTO(**vars(book)) for book in books.items]
    return PaginatedResult[BookDTO](
        items=dto_items,
        total=total_count,
        page=pagination.page,
        size=pagination.size,
        pages=(total_count // pagination.size) + (1 if total_count % pagination.size > 0 else 0),
    )


@router.post("/", response_model=BookDTO, status_code=201)
def create_book(payload: CreateBookDTO):
    """
    Create a new book record.
    """
    book = Book(title=payload.title, author=payload.author, isbn=payload.isbn)
    book_repo.add(book)
    return BookDTO(**vars(book))


@router.post("/lend/{book_id}/{user_id}")
def lend_book(book_id: UUID, user_id: UUID):
    """
    Lend a book to a user. Both the book and user must already exist.
    """
    usecase = LendBookUseCase(book_repo, user_repo)
    try:
        usecase.execute(book_id, user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"status": "success", "book_id": book_id, "lent_to": user_id}


@router.post("/return/{book_id}")
def return_book(book_id: UUID):
    """
    Return a previously lent book.
    """
    usecase = ReturnBookUseCase(book_repo)
    try:
        usecase.execute(book_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"status": "success", "book_id": book_id}