import strawberry
import strawberry.fastapi
from typing import List
from uuid import UUID
from app.adapters.db.repositories import book_repo, user_repo
from app.core.entities.book import Book
from app.core.entities.user import User

@strawberry.type
class BookType:
    id: strawberry.ID
    title: str
    author: str
    isbn: str
    borrower_id: strawberry.ID = None

@strawberry.type
class UserType:
    id: strawberry.ID
    name: str

@strawberry.type
class Query:
    @strawberry.field
    def books(self) -> List[BookType]:
        return [BookType(**book.__dict__) for book in book_repo.list()]

    @strawberry.field
    def users(self) -> List[UserType]:
        return [UserType(**user.__dict__) for user in user_repo.list()]

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_user(self, name: str) -> UserType:
        user = User(name=name)
        user_repo.add(user)
        return UserType(**user.__dict__)

    @strawberry.mutation
    def create_book(self, title: str, author: str, isbn: str) -> BookType:
        book = Book(title=title, author=author, isbn=isbn)
        book_repo.add(book)
        return BookType(**book.__dict__)

    @strawberry.mutation
    def lend_book(self, book_id: strawberry.ID, user_id: strawberry.ID) -> BookType:
        book = book_repo.get(UUID(book_id))
        book.lend_to(UUID(user_id))
        book_repo.update(book)
        return BookType(**book.__dict__)

    @strawberry.mutation
    def return_book(self, book_id: strawberry.ID) -> BookType:
        book = book_repo.get(UUID(book_id))
        book.return_book()
        book_repo.update(book)
        return BookType(**book.__dict__)

schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = strawberry.fastapi.GraphQLRouter(schema)