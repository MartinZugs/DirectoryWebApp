from datetime import datetime
from flaskDemo import db, login_manager
from sqlalchemy import orm
from flask_login import UserMixin

db.Model.metadata.reflect(db.engine)

# Created a seperate User table for login users that could be the system owner etc, not sure if we want to user that or tie to the fake users.

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    
class User(db.Model, UserMixin):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    def serialize(self):
        return {
            'id':self.id,
            'username':self.username,
            'Email': self.email
            }
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
    def serialize(self):
        
        return {
            'EmployeeID': self.EmployeeID,
            'RetirementDate':self.RetirementDate,
            'RetirementPackage': self.RetirementPackage
        }
class Staff(db.Model):
    __table__ = db.Model.metadata.tables['Staff']
    def serialize(self):
        
        return {
            'EmployeeID': self.EmployeeID,
            'OfficeID':self.OfficeID,
            'DepartmentID': self.DepartmentID
        }
class Faculty(db.Model):
    __table__ = db.Model.metadata.tables['Faculty']
    def serialize(self):
        
        return {
            'EmployeeID': self.EmployeeID,
            'OfficeID':self.OfficeID,
            'DepartmentID': self.DepartmentID
        }
class Student(db.Model):
    __table__ = db.Model.metadata.tables['Student']
    def serialize(self):
        
        return {
            'PersonID': self.PersonID,
            'EnrollmentStatus': self.EnrollmentStatus,
            'CreditHoursTotal': self.CreditHoursTotal,
            'StudentType': self.StudentType
        }
class Undergrad(Student):
    __table__ = db.Model.metadata.tables['Undergrad']
    def serialize(self):
        
        return {
            'StudentID': self.StudentID
        }
class Graduate(Student):
    __table__ = db.Model.metadata.tables['Graduate']
    def serialize(self):
        
        return {
            'StudentID': self.StudentID,
            'UGCompDate': self.UGCompDate,
            'GraduateType': self.GraduateType
        }
class Teaching_Assistant(Graduate):
    __table__ = db.Model.metadata.tables['Teaching_Assistant']
    def serialize(self):
        
        return {
            'StudentID': self.StudentID,
            'CourseID': self.CourseID
        }
class Research_Assistant(Graduate):
    __table__ = db.Model.metadata.tables['Research_Assistant']
    def serialize(self):
        
        return {
            'StudentID': self.StudentID,
            'ResearchFocus': self.ResearchFocus
        }
class Alumni(Student):
    __table__ = db.Model.metadata.tables['Alumni']
    def serialize(self):
        
        return {
            'StudentID': self.StudentID,
            'GraduationDate': self.GraduationDate,
            'FinalSemester': self.FinalSemester
        }
class Department(db.Model):
    __table__ = db.Model.metadata.tables['Department']
    def serialize(self):
        
        return {
            'DepartmentID': self.DepartmentID,
            'BuildingID': self.BuildingID,
            'DepartmentName': self.DepartmentName
        }
class Office(db.Model):
    __table__ = db.Model.metadata.tables['Office']
    def serialize(self):
        
        return {
            'OfficeID': self.OfficeID,
            'BuildingID': self.BuildingID
        }
class Building(db.Model):
    __table__ = db.Model.metadata.tables['Building']
    def serialize(self):
        
        return {
            'CampusID': self.CampusID,
            'BuildingName': self.BuildingName,
            'BuildingID': self.BuildingID,
            'BuildingAddress': self.BuildingAddress
        }
class Campus(db.Model):
    __table__ = db.Model.metadata.tables['Campus']
    def serialize(self):
        
        return {
            'CampusID': self.CampusID,
            'CampusName': self.CampusName
        }
class Course(db.Model):
    __table__ = db.Model.metadata.tables['Course']
    def serialize(self):
        
        return {
            'CourseID': self.CourseID,
            'ProfID': self.ProfID,
            'CourseDescription': self.CourseDescription,
            'NoOfSeats': self.NoOfSeats,
            'Credits': self.Credits


        }
class Enrolled_In(db.Model):
    __table__ = db.Model.metadata.tables['Enrolled_In']
    def serialize(self):
        
        return {
            'StudentID': self.StudentID,
            'CourseID': self.CourseID

        }
class Prereqs(db.Model):
    __table__ = db.Model.metadata.tables['Prereqs']
    def serialize(self):
        
        return {
            'MainCourseID': self.MainCourseID,
            'PrereqID': self.PrereqID

        }
class Registered_For(db.Model):
    __table__ = db.Model.metadata.tables['Registered_For']
    def serialize(self):
        
        return {
            'StudentID': self.StudentID,
            'CourseID': self.CourseID
        }
#also just here so i can make sure I did my imports correctly 
# class Student(db.Model):
#     __tablename__='student'
#     studentID = db.Column(db.Integer, primary_key=True)
#     studentName = db.Column(db.String(25))