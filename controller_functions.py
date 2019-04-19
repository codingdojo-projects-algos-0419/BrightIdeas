from flask import render_template,redirect,session,request
from config import db
from models import User,Post

def register_login():
    return render_template("main.html")
    
def create_new_user():
    register_validation = User.register_validations(request.form)
    if register_validation == True:
        new_user = User.add_new_user(request.form)
        session["user_id"] = new_user.id
        return redirect("/bright_ideas")
    else:
        return redirect("/")

def log_in():
    login_validation = User.login_validation(request.form)    
    if login_validation == True:
        session["user_id"] = User.check_login_user(request.form).id
        return redirect("/bright_ideas")
    else:
        return redirect("/")

def log_out():
    session.clear()
    return redirect("/")

def bright_ideas():
    user_info = User.login_user(session["user_id"])
    all_post = Post.all_post()
    return render_template("bright_ideas.html",user_info = user_info,posts = all_post)

def add_post():
    if Post.post_validation(request.form):
        Post.add_new_post(request.form)
    return redirect("/bright_ideas")

def user(user_id):
    user_info = User.login_user(user_id)
    get_user_post = Post.get_user_post(user_id)
    print(get_user_post)
    count_all_post_likes = 0 
    for each_post in get_user_post:
        count_all_post_likes += len(each_post.user_who_like_post)

    print(count_all_post_likes)

    return render_template("user.html",user_info = user_info,count_user_post = len(get_user_post),count_all_post_likes = count_all_post_likes)

def like(post_id):
    Post.add_like(session["user_id"],post_id)
    return redirect("/bright_ideas")

def post(post_id):
    post = Post.get_post(post_id)
    return render_template("post.html",post = post)

def delete(post_id):
    Post.delete_post(post_id)
    return redirect("/bright_ideas")