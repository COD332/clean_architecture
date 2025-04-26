from flask import Blueprint, jsonify, request
from uuid import UUID, uuid4
from app.adapters.db.repositories import book_repo
from app.core.entities.book import Book
from app.core.dtos.book_dto import BookDTO, CreateBookDTO
from app.core.dtos.pagination import PaginationParams, PaginatedResult


book_bp = Blueprint("books", __name__)

@book_bp.route("/", methods=["GET"])
def list_books():
    """
    List all books with pagination.
    """
    pagination = PaginationParams(**request.args)
    paginated_books = book_repo.list(pagination)
    return jsonify(
        PaginatedResult[BookDTO](
            items=[BookDTO(**vars(book)).dict() for book in paginated_books.items],
            total=paginated_books.total,
            page=paginated_books.page,
            size=paginated_books.size,
            pages=paginated_books.pages
        ).dict()
    )

@book_bp.route("/", methods=["POST"])
def create_book():
    """
    Create a new book using repository.
    """
    data = request.get_json()
    dto = CreateBookDTO(**data)
    book = Book(title=dto.title, author=dto.author, isbn=dto.isbn)
    book_repo.add(book)
    return jsonify(BookDTO(**vars(book)).dict()), 201
