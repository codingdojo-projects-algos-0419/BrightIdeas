from config import db,func,EMAIL_REGEX,bcrypt
from flask import flash
import re


likes_table = db.Table('likes',db.Column('user_id', db.Integer, 
                        db.ForeignKey('users.id'), primary_key=True),
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

    @classmethod
    def register_validations(cls,user_data):
        is_valid = True
        #check name no numbers or special characters
        for char in user_data['name']:
            if (ord(char) < 65) or (ord(char) > 122):
                is_valid = False
                flash("Your name should not contain any numbers or special characters","error")
            if (ord(char) >= 91) and (ord(char) <= 96):
                is_valid = False
                flash("Your name should not contain any numbers or special characters","error")


        if len(user_data['name']) < 1: #check name must filled
            flash("Please enter your first name","error")
            is_valid = False
        if len(user_data['alias']) < 1: #check alias must filled
            flash("Please enter your alias","error")
            is_valid = False
        if user_data['pword'] != user_data['confirm']: #check pword must match confirm
            flash("Please check your password again","error")
            is_valid = False
        if not EMAIL_REGEX.match(user_data['email']):    # test whether a field matches the pattern
            flash("Invalid email address!","error")
            is_valid = False
        
        #checking password must has a number and a capital letter
        if len(user_data['pword']) < 5: #check first_password must over 5 characters
            flash("Your password should more than 5 characters","error")
            is_valid = False
        elif re.search('[0-9]',user_data['pword']) is None:
            flash("Make sure your password has a number in it.","error")
            is_valid = False
        elif re.search('[A-Z]',user_data['pword']) is None:
            flash("Make sure your password has a capital letter in it.","error")
            is_valid = False

        ask_for_email = cls.query.all()
        for each_email in ask_for_email:
            if each_email.email == user_data["email"]:
                flash("This email has been registerd!Please use another email","error")
                is_valid = False

        return is_valid

    @classmethod
    def add_new_user(cls,user_data):
        pw_hash = bcrypt.generate_password_hash(user_data['pword']) 
        user_to_add = cls(name=user_data["name"],alias=user_data["alias"],email=user_data["email"],password=pw_hash)
        db.session.add(user_to_add)
        db.session.commit()
        return user_to_add

    @classmethod
    def login_validation(cls,user_data):
        login_user = cls.query.filter_by(email=user_data["email"]).all()
        print("login_user:",login_user)
        is_valid = False
        if login_user:
            if bcrypt.check_password_hash(login_user[0].password, user_data["pword"]):
                is_valid = True
                return is_valid
        flash("You could not be logged in","error")
        return is_valid

    @classmethod
    def check_login_user(cls,user_data):
        login_user = cls.query.filter_by(email=user_data["email"]).all()
        return login_user[0]
    
    @classmethod
    def login_user(cls,user_id):
        login_user = cls.query.filter_by(id = user_id).all()
        return login_user[0]



class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    content = db.Column(db.String(225))
    created_at = db.Column(db.DateTime,server_default=func.now())
    updated_at = db.Column(db.DateTime,server_default=func.now(),onupdate=func.now())
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"),nullable=False)
    user = db.relationship('User',foreign_keys=[user_id],backref="user_Post")
    user_who_like_post = db.relationship('User', secondary=likes_table)

    @classmethod
    def post_validation(cls,user_data):
        if len(user_data["content"]) < 1:
            flash("Please enter the idea","error")
            return False
        else:
            return True

    @classmethod
    def add_new_post(cls,user_data):
        post_to_add = cls(content = user_data["content"],user_id = user_data["user_id"])
        db.session.add(post_to_add)
        db.session.commit()
        return post_to_add

    @classmethod
    def all_post(cls):
        return cls.query.all()
    
    @classmethod
    def get_user_post(cls,user_id):
        get_user_all_post = cls.query.filter_by(user_id = user_id).all()
        return get_user_all_post
    
    @classmethod
    def add_like(cls,user_id,post_id):
        add_like_to_post = cls.query.get(post_id)
        user = User.query.get(user_id)
        add_like_to_post.user_who_like_post.append(user)
        db.session.commit()
    
    @classmethod
    def get_post(cls,post_id):
        get_single_post = cls.query.filter_by(id = post_id).first()
        return get_single_post

    @classmethod
    def delete_post(cls,post_id):
        get_single_post = cls.query.get(post_id)
        db.session.delete(get_single_post)
        db.session.commit()

        


        