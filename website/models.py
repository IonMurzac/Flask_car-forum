# Import all the necessary libraries and packages
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import Column, ForeignKey, Integer, Unicode
from sqlalchemy.orm import relationship


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(), default=func.now())
    about = db.Column(db.String(300), nullable=False)
    city = db.Column(db.String(150), nullable=False)
    car = db.Column(db.String(150), nullable=False)
    hobby = db.Column(db.String(150))
    file = db.Column(db.String(300))
    posts = db.relationship("Post", backref = "User", passive_deletes=True)
    comments = db.relationship("Comment", backref = "User", passive_deletes=True)
    likes = db.relationship("Like", backref = "User", passive_deletes=True)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime(), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    comments = db.relationship("Comment", backref = "Post", passive_deletes=True)
    likes = db.relationship("Like", backref = "Post", passive_deletes=True)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(300), nullable=False)
    date_created = db.Column(db.DateTime(), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id", ondelete="CASCADE"), nullable=False)


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id", ondelete="CASCADE"), nullable=False)