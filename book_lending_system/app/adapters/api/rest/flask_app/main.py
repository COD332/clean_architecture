from flask import Flask
from app.adapters.api.rest.flask_app.routers.book_router import book_bp
from app.adapters.api.rest.flask_app.routers.user_router import user_bp

def create_app():
    app = Flask(__name__)

    app.config["JSON_SORT_KEYS"] = False

    app.register_blueprint(book_bp, url_prefix="/books")
    app.register_blueprint(user_bp, url_prefix="/users")

    return app
