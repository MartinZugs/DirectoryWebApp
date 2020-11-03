# essentially I switched to how the professor layed out 08-crud
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# app setup goes here
app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'


db = SQLAlchemy(app) #setup db

from flaskDemo import routes
# from models import models
