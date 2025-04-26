from fastapi import APIRouter, Depends
from typing import List
from app.core.entities.user import User
from app.core.dtos.user_dto import UserDTO
from app.adapters.db.repositories import user_repo
from app.core.dtos.pagination import PaginationParams, PaginatedResult


router = APIRouter()

@router.post("/", response_model=UserDTO)
def create_user(payload: UserDTO):
    user = User(name=payload.name, id=payload.id)
    user_repo.add(user)
    return payload

@router.get("/", response_model=PaginatedResult[UserDTO])
def list_users(pagination: PaginationParams = Depends(PaginationParams)):
    """
    List all users with pagination.
    """
    users = user_repo.list(pagination)
    total_count = len(users.items)
    dto_items = [UserDTO(**vars(user)) for user in users.items]
    return PaginatedResult[UserDTO](
        items=dto_items,
        total=total_count,
        page=pagination.page,
        size=pagination.size,
        pages=(total_count // pagination.size) + (1 if total_count % pagination.size > 0 else 0),
    )