from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class PaperRead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(10000))
    authors = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class PaperToRead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(10000))
    authors = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150), unique=True)
    papers_read = db.relationship('PaperRead')
    papers_to_read = db.relationship('PaperToRead')
