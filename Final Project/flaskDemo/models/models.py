#probably temporary since I will want to split this apart later for legibility
from enum import unique
from sqlalchemy.sql.schema import Column, ForeignKey
from .flaskDemo import db
from flask_sqlalchemy import SQLAlchemy


# I think a lot of these need nullable
class Person(db.Model):
    id            = db.Column(db.Integer, primary_key = True)
    first_name    = db.Column(db.String(25))
    last_name     = db.Column(db.String(30))
    email         = db.Column(db.String(255), unique = True, nullable = False)
    phone_numbers = db.relationship("person_phone_numbers") #ref to phone numbers
    person_type   = db.Column(db.String(50))

    __mapper_args__ = { # this is what lets it have subtypes
        'polymorphic_identity':'person',
        'polymorphic_on':person_type
    }

class Employee(Person):
    __tablename__ = 'employee'
    id            = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key = True) #all of sub types need this
    # possibly need managerID to add the manager relationship
    employee_type = db.Column(db.String(50)) # i wonder if a char can be used

    __mapper_args__ = {
        'polymorphic_identity': 'employee',
        'polymorphic_on'      : 'employee_type'
    }

class Retiree(Employee):
    __tablename__      = 'retiree'
    id                 = db.Column(db.Integer, db.ForeignKey('employee.id'), primary_key = True) 
    retirement_date    = db.Column(db.Date)
    retirement_package = db.Column(db.String(255)) 
    __mapper_args__    = {
        'polymorphic_identity': 'retiree'
    }

class Student(Person):
    __tablename__ = 'student'
    id            = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key = True)
    enrollment_status = db.column(db.String(20))
    credit_hours_total = db.column(db.Integer)
    student_type       = db.column(db.String(50)) #also might be able to be char

    __mapper_args__    = {
        'polymorphic_identity': 'student',
        'polymorphic_on'      : 'student_type'
    }

# multivalued attribute
class PersonPhoneNumber(db.Model):
    __tablename__='person_phone_numbers'
    id = db.Column(db.Integer, db.ForeignKey('person.id'),primary_key = True )
    phone_number = db.Column(db.String(10))


#also just here so i can make sure I did my imports correctly 
class Student(db.Model):
    __tablename__='student'
    studentID = db.Column(db.Integer, primary_key=True)
    studentName = db.Column(db.String(25))