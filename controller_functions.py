from flask import render_template,redirect,session,request
from config import db

#test
def test():
    return render_template("test.html")