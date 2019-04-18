from config import db,func,EMAIL_REGEX,bcrypt
from flask import flash
import re


likes_table = db.Table('likes', 
                       db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
                       db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True))

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(225))
    alias = db.Column(db.String(225))
    email = db.Column(db.String(225))
    password = db.Column(db.String(225)) 
    created_at = db.Column(db.DateTime,server_default=func.now())
    updated_at = db.Column(db.DateTime,server_default=func.now(),onupdate=func.now())
    post_which_user_like = db.relationship('Post', secondary=likes_table)

class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    content = db.Column(db.String(225))
    created_at = db.Column(db.DateTime,server_default=func.now())
    updated_at = db.Column(db.DateTime,server_default=func.now(),onupdate=func.now())
    user_who_like_post = db.relationship('User', secondary=likes_table)
