# essentially I switched to how the professor layed out 08-crud
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# app setup goes here
app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://Team5:453Team5@45.55.59.121/Team5'


db = SQLAlchemy(app) #setup db

from flaskDemo import routes
from flaskDemo import models

models.db.create_all()
