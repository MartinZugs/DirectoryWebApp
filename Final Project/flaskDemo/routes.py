import os
import secrets
from flask import render_template, url_for, flash, redirect, request
from flaskDemo import app, db, bcrypt
from flaskDemo.models import Person, User
from flaskDemo.forms import RegistrationForm, LoginForm, SearchForm, ContactForm, ContactUpdateForm
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime


#moved the code from flaskdemo.py here since this will be the routes

@app.route("/")
@app.route("/home")
def home():
    results = Person.query.all()
    return render_template('home.html', title='Home',allpersons=results)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    
    if current_user.is_authenticated:
        flash('You are already logged in!', 'danger')
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/search", methods=['GET', 'POST'])
def search():
    return render_template('search.html', title='Search')

@app.route("/contact/<PersonID>")
@login_required
def contact(PersonID):
    contact = Person.query.get_or_404(PersonID)
    return render_template('contact.html', title=str(contact.FName)+"_"+str(contact.LName), contact=contact, now=datetime.utcnow())

@app.route("/result", methods=['GET', 'POST'])
def result():
    form = SearchForm()
    return render_template('result.html', title='Result', form=form)

@app.route("/admin", methods=['GET', 'POST'])
def admin():
    
    return render_template('admin.html', title='Admin')

@app.route("/settings", methods=['GET', 'POST'])
def settings():
    
    return render_template('settings.html', title='Settings')

@app.route("/detail", methods=['GET', 'POST'])
def detail():
    
    return render_template('detail.html', title='Detail')

@app.route("/error", methods=['GET', 'POST'])
def error():
    
    return render_template('error.html', title='Error')
    
@app.route("/contact/new", methods=['GET', 'POST'])
@login_required
def new_contact():

    # only allow those who are marked as managers, our version of admins, to add new people
    current_contact = Person.query.filter_by(Email=current_user._get_current_object().email).first()

    if current_contact == None:

        flash('You are not allowed to add a new entry', 'danger')
        return redirect(url_for('home'))

    elif current_contact.Manager == 0:
        
        flash('You are not allowed to add a new entry', 'danger')
        return redirect(url_for('home'))

    form = ContactForm()
    if form.validate_on_submit():
        contact = Person(FName=form.FName.data, LName=form.LName.data, Email=form.Email.data, PhoneNum=form.PhoneNum.data, UserType=form.UserType.data, Manager=form.Manager.data)
        db.session.add(contact)
        db.session.commit()
        flash('You have added a new contact!', 'success')
        return redirect(url_for('home'))
    return render_template('createcontact.html', title='New Contact',
                           form=form, legend='New Contact')
                           

@app.route("/contact/<PersonID>/delete",methods=['POST'])
@login_required
def deletecontact(PersonID):
    
    delcontact = Person.query.get_or_404(PersonID)
    user = User.query.filter_by(email=delcontact.Email).first()
    
    # only allow those who are marked as managers, our version of admins, to delete everyone 
    current_contact = Person.query.filter_by(Email=current_user._get_current_object().email).first()

    if current_contact == None:

        pass

    # If you are logged in not as a manager, process as a normal account. This means if you are a manager you are allowed by default
    elif current_contact.Manager == 0:

        # If the user does not exist or if you are not the same user as the entry you are trying to delete, reject
        if user == None:

            flash('You are not allowed to delete this entry', 'danger')
            return redirect(url_for('home'))

        elif user.email != current_user._get_current_object().email:

            flash('You are not allowed to delete this entry', 'danger')
            return redirect(url_for('home'))

    db.session.delete(delcontact)
    db.session.commit()
    flash('The contact has been removed!', 'success')
    return redirect(url_for('home'))
    
@app.route("/contact/<PersonID>/update", methods=['GET', 'POST'])
@login_required
def updatecontact(PersonID):
    print()
    contact = Person.query.get_or_404(PersonID)
    currentContact =  Person.PersonID
    user = User.query.filter_by(email=contact.Email).first()

    # only allow those who are marked as managers, our version of admins, to update everyone 
    current_contact = Person.query.filter_by(Email=current_user._get_current_object().email).first()

    if current_contact == None:

        pass

    # If you are logged in not as a manager, process as a normal account. This means if you are a manager you are allowed by default
    elif current_contact.Manager == 0:

        # If the user does not exist or if you are not the same user as the entry you are trying to edit, reject
        if user == None:

            flash('You are not allowed to edit this entry', 'danger')
            return redirect(url_for('home'))

        elif user.email != current_user._get_current_object().email:

            flash('You are not allowed to edit this entry', 'danger')
            return redirect(url_for('home'))
 
    form = ContactUpdateForm()
    if form.validate_on_submit():
        if currentContact != form.PersonID.data:
            contact.PersonID = form.PersonID.data
        contact.FName = form.FName.data
        contact.LName = form.LName.data
        contact.Email = form.Email.data
        contact.PhoneNum = form.PhoneNum.data
        contact.UserType = form.UserType.data
        db.session.commit()
        flash ('The contact has been updated!', 'success')
        return redirect (url_for ('contact', PersonID=PersonID))
    elif request.method == 'GET':
        form.PersonID.data = contact.PersonID
        form.FName.data = contact.FName
        form.LName.data = contact.LName
        form.Email.data = contact.Email
        form.PhoneNum.data = contact.PhoneNum
        form.UserType.data = contact.UserType
    return render_template ('updatecontact.html', title='Update Contact', form=form, legend='Update Contact')