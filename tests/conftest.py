import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import pytest

from rate_my_game import create_app
from rate_my_game.database import db
from rate_my_game.models import Game, GameTag, PREDEFINED_TAGS


@pytest.fixture()
def app(tmp_path):
    test_db_path = tmp_path / "test_database.db"

    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{test_db_path}",
        }
    )

    with app.app_context():
        db.drop_all()
        db.create_all()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def sample_game(app):
    with app.app_context():
        game = Game(name="Test Game", company="Test Company")
        db.session.add(game)
        db.session.commit()

        for tag in PREDEFINED_TAGS:
            game_tag = GameTag(game_id=game.id, tag_name=tag, count=0)
            db.session.add(game_tag)

        db.session.commit()

        return game.id