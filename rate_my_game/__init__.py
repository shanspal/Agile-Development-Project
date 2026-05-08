from flask import Flask
from .database import db, init_db
from .routes import register_routes

def create_app(test_config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "dev-secret-key"

    if test_config is None:
        app.config.update(test_config)

    db.init_app(app)
    init_db(app)
    register_routes(app)

    return app
