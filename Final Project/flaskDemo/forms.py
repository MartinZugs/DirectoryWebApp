from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, PasswordField, SelectField, SubmitField, BooleanField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo,ValidationError
from flaskDemo import db
from flaskDemo.models import Person, Student, Employee



class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class SearchForm(FlaskForm):
    submit =SubmitField('Search')
    
class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class ContactUpdateForm(FlaskForm):

    PersonID = HiddenField("")
    FName = StringField('First Name:', validators=[DataRequired(),Length(max=25)])
    LName = StringField('Last Name:', validators=[DataRequired(),Length(max=25)])
    Email = StringField('Email:', validators=[DataRequired(),Length(max=30)])
    PhoneNum = StringField('Phone:', validators=[DataRequired(),Length(max=20)])
    UserType = HiddenField("")
    Manager = HiddenField("")
    StudentID = HiddenField("")
    StudentType = HiddenField("")
    EnrollmentStatus = HiddenField("")
    
    
    submit = SubmitField('Update this users directory entry')
    
class ContactForm(ContactUpdateForm):

    EmployeeType= SelectField('Employee Type:', choices=[('Staff','Staff'),('Faculty','Faculty')])
    Manager= SelectField(' Is a Manager:', choices=[(1,'Yes'),(0,'No')],coerce=int)
    ManagerID = SelectField('Reports To:', choices=[(1,'Frank Zab'),(4,'Eric Testing'),(9,'Martin Zugschwert'),(10,'Eric Killham')], coerce=int )
    submit = SubmitField('Add this contact') 
    
    def validate_PersonID(self, PersonID):  
        checkID = Person.query.filter_by(PersonID=PersonID.data).first()
        if checkID:
           raise ValidationError('That employee ID is already in user. Please verify and enter a different one.')
           

           
class StudentForm(ContactUpdateForm):

    StudentType = SelectField('Student Type:', choices=[('Undergrad','Undergrad'),('Graduate','Graduate')])
    EnrollmentStatus = SelectField('Enrollment Status:', choices=[('Full-time','Full-time'),('Part-time','Part-time')])
    submit = SubmitField('Add this contact') 
    
    def validate_PersonID(self, StudentID):  
        checkID = Student.query.filter_by(StudentID=StudentID.data).first()
        if checkID:
           raise ValidationError('That Student ID is already in user. Please verify and enter a different one.')

