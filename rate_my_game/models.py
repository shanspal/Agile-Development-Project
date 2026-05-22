from datetime import datetime
from .database import db

PREDEFINED_TAGS = [
    "Action",
    "RPG",
    "Multiplayer",
    "Singleplayer",
    "Story-Rich",
    "Casual",
    "Competitive",
    "Puzzle",
    "Horror",
    "Open World",
    "Indie",
    "Strategy",
]


class Game(db.Model):
    __tablename__ = "games"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    company = db.Column(db.String(120), nullable=False)
    image_url = db.Column(db.String(500), nullable=True)
    description = db.Column(db.Text, nullable=True)

    ratings = db.relationship("Rating", backref="game", lazy=True, cascade="all, delete-orphan")
    tags = db.relationship("GameTag", backref="game", lazy=True, cascade="all, delete-orphan")

    def average_gameplay(self):
        if not self.ratings:
            return None
        return sum(r.gameplay for r in self.ratings) / len(self.ratings)

    def average_difficulty(self):
        if not self.ratings:
            return None
        return sum(r.difficulty for r in self.ratings) / len(self.ratings)

    def total_tag_votes(self):
        return sum(t.count for t in self.tags)


class Rating(db.Model):
    __tablename__ = "ratings"

    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey("games.id"), nullable=False)
    gameplay = db.Column(db.Integer, nullable=False)      # 1–5
    difficulty = db.Column(db.Integer, nullable=False)    # 1–5
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class GameTag(db.Model):
    __tablename__ = "game_tags"

    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey("games.id"), nullable=False)
    tag_name = db.Column(db.String(50), nullable=False)
    count = db.Column(db.Integer, default=0, nullable=False)

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)