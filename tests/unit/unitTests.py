import pytest
from rate_my_game.database import db
from rate_my_game.models import Game, Rating, GameTag

class TestGameModel:
    def test_create_game(self, app):
        with app.app_context():
            game = make_game()
            fetched = db.session.get(Game, game.id)
            assert fetched is not None
            assert fetched.name    == "Test Game"
            assert fetched.company == "Acme Studios"

    def test_game_requires_name(self, app):
        with app.app_context():
            with pytest.raises(Exception):
                db.session.add(Game(company="Acme"))
                db.session.commit()

    def test_game_requires_company(self, app):
        with app.app_context():
            with pytest.raises(Exception):
                db.session.add(Game(name="No Company"))
                db.session.commit()



class TestRatingModel:

    def test_create_rating(self, app):
        with app.app_context():
            game   = make_game()
            rating = add_rating(game.id, gameplay=5, difficulty=2)
            assert rating.id         is not None
            assert rating.gameplay   == 5
            assert rating.difficulty == 2
            assert rating.game_id    == game.id

    def test_rating_created_at_set_automatically(self, app):
        from datetime import datetime
        with app.app_context():
            game   = make_game()
            before = datetime.utcnow()
            rating = add_rating(game.id, gameplay=3, difficulty=3)
            after  = datetime.utcnow()
            assert before <= rating.created_at <= after


    def test_rating_requires_game_id(self, app):
        with app.app_context():
            with pytest.raises(Exception):
                db.session.add(Rating(gameplay=3, difficulty=3))
                db.session.commit()



class TestGameTagModel:

    def test_create_tag(self, app):
        with app.app_context():
            game = make_game()
            tag  = add_tag(game.id, "Indie", count=7)
            assert tag.id       is not None
            assert tag.tag_name == "Indie"
            assert tag.count    == 7
            assert tag.game_id  == game.id

    def test_tag_default_count(self, app):
        with app.app_context():
            game = make_game()
            tag  = GameTag(game_id=game.id, tag_name="Casual")
            db.session.add(tag)
            db.session.commit()
            assert tag.count == 0

    def test_tag_requires_game_id(self, app):
        with app.app_context():
            with pytest.raises(Exception):
                db.session.add(GameTag(tag_name="RPG", count=1))
                db.session.commit()

    def test_tag_requires_tag_name(self, app):
        with app.app_context():
            game = make_game()
            with pytest.raises(Exception):
                db.session.add(GameTag(game_id=game.id, count=1))
                db.session.commit()

