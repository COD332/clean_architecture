from app.core.entities.book import Book
from app.core.entities.user import User
from app.core.repositories.book_repository import BookRepository
from app.core.repositories.user_repository import UserRepository
from app.core.dtos.pagination import PaginationParams, PaginatedResult
from app.adapters.db.sqlalchemy import SessionLocal, Base, engine
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey
from typing import Optional

class BookModel(Base):
    __tablename__ = "books"
    id = Column(UUID, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    isbn = Column(String, unique=True, index=True)
    borrower_id = Column(UUID, ForeignKey("users.id"), nullable=True)

class UserModel(Base):
    __tablename__ = "users"
    id = Column(UUID, primary_key=True, index=True)
    name = Column(String, index=True)

def book_to_model(book: Book) -> BookModel:
    return BookModel(
        id=book.id,
        title=book.title,
        author=book.author,
        isbn=book.isbn,
        borrower_id=book.borrower_id
    )
def model_to_book(model: BookModel) -> Book:
    return Book(
        id=model.id,
        title=model.title,
        author=model.author,
        isbn=model.isbn,
        borrower_id=model.borrower_id
    )
def user_to_model(user: User) -> UserModel:
    return UserModel(
        id=user.id,
        name=user.name,
    )
def model_to_user(model: UserModel) -> User:
    return User(
        id=model.id,
        name=model.name,
    )

class PostgresBookRepository(BookRepository):
    def __init__(self):
        self.db = SessionLocal()

    def add(self, book: Book) -> None:
        db_book = book_to_model(book)
        self.db.add(db_book)
        self.db.commit()

    def get(self, book_id: UUID) -> Optional[Book]:
        db_book = self.db.query(BookModel).filter(BookModel.id == book_id).first()
        return model_to_book(db_book) if db_book else None

    def list(self, params: PaginationParams) -> PaginatedResult[Book]:
        items = self.db.query(BookModel).all()
        total = len(items)
        start = (params.page - 1) * params.size
        end = start + params.size
        paginated_items = items[start:end]
        pages = (total + params.size - 1) // params.size
        return PaginatedResult(
            items=[model_to_book(item) for item in paginated_items],
            total=total,
            page=params.page,
            size=params.size,
            pages=pages
        )

    def update(self, book: Book) -> None:
        db_book = self.db.query(BookModel).filter(BookModel.id == book.id).first()
        if db_book:
            db_book.title = book.title
            db_book.author = book.author
            db_book.isbn = book.isbn
            db_book.borrower_id = book.borrower_id
            self.db.commit()

class PostgresUserRepository(UserRepository):
    def __init__(self):
        self.db = SessionLocal()

    def add(self, user: User) -> None:
        db_user = user_to_model(user)
        self.db.add(db_user)
        self.db.commit()

    def get(self, user_id: UUID) -> Optional[User]:
        db_user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        return model_to_user(db_user) if db_user else None

    def list(self, params: PaginationParams) -> PaginatedResult[User]:
        items = self.db.query(UserModel).all()
        total = len(items)
        start = (params.page - 1) * params.size
        end = start + params.size
        paginated_items = items[start:end]
        pages = (total + params.size - 1) // params.size
        return PaginatedResult(
            items=[model_to_user(item) for item in paginated_items],
            total=total,
            page=params.page,
            size=params.size,
            pages=pages
        )

    def update(self, user: User) -> None:
        db_user = self.db.query(UserModel).filter(UserModel.id == user.id).first()
        if db_user:
            db_user.name = user.name
            self.db.commit()

# Initialize the database
Base.metadata.create_all(bind=engine)

book_repo = PostgresBookRepository()
user_repo = PostgresUserRepository()