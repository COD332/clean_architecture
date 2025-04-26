from pydantic import BaseModel
from typing import Generic, TypeVar, List

T = TypeVar("T")

class PaginationParams(BaseModel):
    page: int = 1
    size: int = 20

class PaginatedResult(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
    pages: int
    
    class Config:
        arbitrary_types_allowed = True