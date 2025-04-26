import redis
import json
from app.core.repositories.book_repository import BookRepository
from app.core.repositories.user_repository import UserRepository
from app.core.dtos.pagination import PaginationParams, PaginatedResult
from app.core.entities.book import Book
from app.core.entities.user import User
from app.config import REDIS_HOST, REDIS_PORT, REDIS_DB

redis_client = redis.StrictRedis(host=REDIS_HOST, port=int(REDIS_PORT), db=int(REDIS_DB))

class RedisBookRepository(BookRepository):
    def add(self, book: Book) -> None:
        redis_client.set("book-" + str(book.id), json.dumps(book.to_dict()))

    def get(self, book_id: str) -> Book:
        book_data = redis_client.get("book-" + str(book_id))
        if book_data:
            return Book.from_dict(json.loads(book_data))
        return None

    def list(self, pagination: PaginationParams) -> PaginatedResult[Book]:
        keys = redis_client.keys()
        book_keys = [key for key in keys if key.startswith(b'book-')]
        books = []
        for key in book_keys:
            book_data = redis_client.get(key)
            if book_data:
                books.append(Book.from_dict(json.loads(book_data)))
        
        total = len(books)
        start = (pagination.page - 1) * pagination.size
        end = start + pagination.size
        paginated_books = books[start:end]
        pages = (total + pagination.size - 1) // pagination.size
        
        return PaginatedResult(
            items=paginated_books,
            total=total,
            page=pagination.page,
            size=pagination.size,
            pages=pages
        )
    
    def update(self, book: Book) -> None:
        redis_client.set("book-" + str(book.id), json.dumps(book.to_dict()))

class RedisUserRepository(UserRepository):
    def add(self, user: User) -> None:
        redis_client.set("user-" + str(user.id), json.dumps(user.to_dict()))

    def get(self, user_id: str) -> User:
        user_data = redis_client.get("user-" + str(user_id))
        if user_data:
            return User.from_dict(json.loads(user_data))
        return None

    def list(self, pagination: PaginationParams) -> PaginatedResult[User]:
        keys = redis_client.keys()
        user_keys = [key for key in keys if key.startswith(b'user-')]
        users = []
        for key in user_keys:
            user_data = redis_client.get(key)
            if user_data:
                users.append(User.from_dict(json.loads(user_data)))
        
        total = len(users)
        start = (pagination.page - 1) * pagination.size
        end = start + pagination.size
        paginated_users = users[start:end]
        pages = (total + pagination.size - 1) // pagination.size
        
        return PaginatedResult(
            items=paginated_users,
            total=total,
            page=pagination.page,
            size=pagination.size,
            pages=pages
        )

# **Single, shared instances**:
book_repo = RedisBookRepository()
user_repo = RedisUserRepository()