import os
import secrets
from flask import render_template, url_for, flash, redirect, request
from flaskDemo import app, db
from flaskDemo.models import Person
from flaskDemo.forms import RegistrationForm, LoginForm, SearchForm, ContactForm, ContactUpdateForm
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
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/search", methods=['GET', 'POST'])
def search():
    return render_template('search.html', title='Search')

@app.route("/contact/<PersonID>")
#@login_required
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
#@login_required
def new_contact():
    form = ContactForm()
    if form.validate_on_submit():
        contact = Person(PersonID=form.PersonID.data, FName=form.FName.data, LName=form.LName.data, Email=form.Email.data, PhoneNum=form.PhoneNum.data, UserType=form.UserType.data, Manager=form.Manager.data)
        db.session.add(contact)
        db.session.commit()
        flash('You have added a new contact!', 'success')
        return redirect(url_for('home'))
    return render_template('createcontact.html', title='New Contact',
                           form=form, legend='New Contact')
                           

@app.route("/contact/<PersonID>/delete",methods=['POST'])
#@login_required
def deletecontact(PersonID):
    delcontact = Person.query.get_or_404(PersonID)
    db.session.delete(delcontact)
    db.session.commit()
    flash('The contact has been removed!', 'success')
    return redirect(url_for('home'))
    
@app.route("/contact/<PersonID>/update", methods=['GET', 'POST'])
#@login_required
def updatecontact(PersonID):
    contact = Person.query.get_or_404(PersonID)
    currentContact =  Person.PersonID
 
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