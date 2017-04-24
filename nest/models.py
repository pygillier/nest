from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy


# DB handler
db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    picture = db.Column(db.String(120))

    def __init__(self, username, email, picture):
        self.username = username
        self.email = email
        self.picture = picture

    def __repr__(self):
        return '<User %r>' % self.username
