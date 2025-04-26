from app.adapters.api.rest.fastapi_app.routers.book_router import router as book_router
from app.adapters.api.rest.fastapi_app.routers.user_router import router as user_router

__all__ = ["book_router", "user_router"]