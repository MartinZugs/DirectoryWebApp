from datetime import datetime
from flaskDemo import db #add login_manager for login stuff below
#from enum import unique
#from sqlalchemy.sql.schema import Column, ForeignKey
#from flask_sqlalchemy import SQLAlchemy
#from flask_login import UserMixin



db.Model.metadata.reflect(db.engine)

# Created a seperate User table for login users that could be the system owner etc, not sure if we want to user that or tie to the fake users.

#@login_manager.user_loader
#def load_user(user_id):
#    return Person.query.get(int(user_id))
    
#class User(db.Model, UserMixin):
#    __table_args__ = {'extend_existing': True}
#    user_id = db.Column(db.Integer, primary_key=True)
#    username = db.Column(db.String(20), unique=True, nullable=False)
#    email = db.Column(db.String(120), unique=True, nullable=False)
#    password = db.Column(db.String(60), nullable=False)

#    def __repr__(self):
#        return f"User('{self.username}', '{self.email}')"

class Person(db.Model):
    __table__ = db.Model.metadata.tables['Person']
    def serialize(self):
        return {
            'PersonID':self.PersonID,
            'FName':self.FName,
            'LName': self.LName,
            'Email': self.Email,
            'UserType': self.UserType,
            "PhoneNum": self.PhoneNum,
            'Manager': self.Manager
            }
    
class Employee(db.Model):
    __table__ = db.Model.metadata.tables['Employee']
    def serialize(self):
        
        return {
            'PersonID':self.PersonID,
            'EmployeeID': self.EmployeeID,
            'ManagerID':self.ManagerID,
            'EmployeeType': self.EmployeeType
        }

class Retiree(db.Model):
    __table__ = db.Model.metadata.tables['Retiree']

class Staff(db.Model):
    __table__ = db.Model.metadata.tables['Staff']

class Faculty(db.Model):
    __table__ = db.Model.metadata.tables['Faculty']

class Student(db.Model):
    __table__ = db.Model.metadata.tables['Student']

class Undergrad(Student):
    __table__ = db.Model.metadata.tables['Undergrad']

class Graduate(Student):
    __table__ = db.Model.metadata.tables['Graduate']

class Teaching_Assistant(Graduate):
    __table__ = db.Model.metadata.tables['Teaching_Assistant']

class Research_Assistant(Graduate):
    __table__ = db.Model.metadata.tables['Research_Assistant']

class Alumni(Student):
    __table__ = db.Model.metadata.tables['Alumni']

class Department(db.Model):
    __table__ = db.Model.metadata.tables['Department']

class Office(db.Model):
    __table__ = db.Model.metadata.tables['Office']

class Building(db.Model):
    __table__ = db.Model.metadata.tables['Building']

class Campus(db.Model):
    __table__ = db.Model.metadata.tables['Campus']

class Course(db.Model):
    __table__ = db.Model.metadata.tables['Course']

class Enrolled_In(db.Model):
    __table__ = db.Model.metadata.tables['Enrolled_In']

class Prereqs(db.Model):
    __table__ = db.Model.metadata.tables['Prereqs']

#also just here so i can make sure I did my imports correctly 
# class Student(db.Model):
#     __tablename__='student'
#     studentID = db.Column(db.Integer, primary_key=True)
#     studentName = db.Column(db.String(25))