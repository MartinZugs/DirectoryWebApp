from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, PasswordField, SelectField, SubmitField, BooleanField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo,ValidationError
from flaskDemo import db
from flaskDemo.models import Person


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
    UserType = SelectField(' University Status:', choices=[('Student','Student'),('Employee','Employee')])
    Manager = HiddenField("")
    
    submit = SubmitField('Update this users directory entry')
    
class ContactForm(ContactUpdateForm):

    PersonID=IntegerField('User ID Number:', validators=[DataRequired()])
    Manager= SelectField(' Is a Manager:', choices=[('1','Yes'),('0','No')])
    submit = SubmitField('Add this contact') 
    
    def validate_PersonID(self, PersonID):  
        checkID = Person.query.filter_by(PersonID=PersonID.data).first()
        if checkID:
           raise ValidationError('That employee ID is already in user. Please verify and enter a different one.')
