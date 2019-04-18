from flask import Flask
from flask_sqlalchemy import SQLAlchemy	
from flask_bcrypt import Bcrypt
from sqlalchemy.sql import func 
from flask_migrate import Migrate
import re

app = Flask(__name__)
app.secret_key="hello world"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///BrightIdeas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)