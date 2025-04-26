from flask import Blueprint, request, jsonify
from app.core.entities.user import User
from app.core.dtos.user_dto import UserDTO
from app.adapters.db.repositories import user_repo
from app.core.dtos.pagination import PaginationParams, PaginatedResult
from uuid import uuid4

user_bp = Blueprint("users", __name__)

@user_bp.route("/", methods=["POST"])
def create_user():
    data = request.get_json()
    dto = UserDTO(**data)
    user = User(name=dto.name, id=dto.id or uuid4())
    user_repo.add(user)
    return jsonify(dto.dict()), 201

@user_bp.route("/", methods=["GET"])
def list_users():
    """
    List all users with pagination.
    """
    pagination = PaginationParams(**request.args)
    paginated_users = user_repo.list(pagination)
    return jsonify(
        PaginatedResult[UserDTO](
            items=[UserDTO(**vars(user)).dict() for user in paginated_users.items],
            total=paginated_users.total,
            page=paginated_users.page,
            size=paginated_users.size,
            pages=paginated_users.pages
        ).dict()
    )
