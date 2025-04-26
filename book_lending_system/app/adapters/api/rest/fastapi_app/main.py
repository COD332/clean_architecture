from fastapi import FastAPI
from app.adapters.api.rest.fastapi_app.routers import book_router, user_router
from app.adapters.api.graphql.schema import graphql_app

app = FastAPI(
    title="Book Lending System",
    version="1.0.0",
    description="API for managing book lending operations",
)

# REST endpoints
app.include_router(book_router, prefix="/books", tags=["books"])
app.include_router(user_router, prefix="/users", tags=["users"])

app.include_router(graphql_app, prefix="/graphql", tags=["graphql"])

# Swagger UI available at /docs and Redoc at /redoc