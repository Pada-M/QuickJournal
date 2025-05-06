from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import func


db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    entries = db.relationship("JournalEntry", backref="author", lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"


class JournalEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    mood = db.Column(db.String(100))
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=func.now())

    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=True
    )  # will be added later

    def __repr__(self):
        return f"<JournalEntry {self.title}>"
