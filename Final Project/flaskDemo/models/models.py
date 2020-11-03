#probably temporary since I will want to split this apart later for legibility
from flaskDemo import db

#also just here so i can make sure I did my imports correctly 
class Student(db.Model):
    __tablename__='student'
    studentID = db.Column(db.Integer, primary_key=True)
    studentName = db.Column(db.String(25))