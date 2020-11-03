from flask import render_template, url_for, flash, redirect
from flaskDemo import app, db
from flaskDemo.forms import RegistrationForm, LoginForm, SearchForm
from .models.models import Student

#moved the code from flaskdemo.py here since this will be the routes

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Martin Zugschwert')


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

