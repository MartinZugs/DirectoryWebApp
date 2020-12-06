import os
import secrets

from flask import render_template, url_for, flash, redirect, request, jsonify
from flask.globals import session
from flaskDemo import app, db, bcrypt
from flaskDemo.models import Person, User, Student, Employee, Faculty, Staff, Department, Office, Building, Campus, Course, Enrolled_In, Registered_For
from flaskDemo.forms import RegistrationForm, LoginForm, SearchForm, ContactForm, ContactUpdateForm, StudentForm
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
import json


#moved the code from flaskdemo.py here since this will be the routes

@app.route("/")
@app.route("/home")
def home():
    results = db.engine.execute(f"SELECT * FROM Person")

    results = results.fetchall()
    
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

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))
    
@app.route("/search", methods=['GET', 'POST'])
def search():
    return render_template('search.html', title='Search')

@app.route("/contact/<PersonID>")
@login_required
def contact(PersonID):
    contact = Person.query.get_or_404(PersonID)

    if contact.UserType == 'Employee':

        employee = Employee.query.filter_by(PersonID=contact.PersonID).first()
        
        # All of this error catching is to avoid any possible problems causing the site to crash
        try:
            if employee.EmployeeType == "Faculty":
                try:
                    faculty = Faculty.query.filter_by(EmployeeID=employee.EmployeeID).first()
                except:
                    faculty = None

                try:
                    department = Department.query.filter_by(DepartmentID=faculty.DepartmentID).first()
            
                except:
                    department = None
            
                try:
                    office = Office.query.filter_by(OfficeID=faculty.OfficeID).first()
            
                except:
                    office = None
            
                try:
                    building = Building.query.filter_by(BuildingID=office.BuildingID).first()
                
                except:
                    building = None

                try:
                    campus = Campus.query.filter_by(CampusID=building.CampusID).first()

                except:
                    campus = None
            
                try:
                    course = Course.query.filter_by(ProfID=faculty.EmployeeID).first()

                except:
                    course = None
                    
            elif employee.EmployeeType == "Staff":
                try:
                    staff = Staff.query.filter_by(EmployeeID=employee.EmployeeID).first()
                except:
                    staff = None

                try:
                    department = Department.query.filter_by(DepartmentID=staff.DepartmentID).first()
            
                except:
                    department = None
            
                try:
                    office = Office.query.filter_by(OfficeID=staff.OfficeID).first()
            
                except:
                    office = None
            
                try:
                    building = Building.query.filter_by(BuildingID=office.BuildingID).first()
                
                except:
                    building = None

                try:
                    campus = Campus.query.filter_by(CampusID=building.CampusID).first()

                except:
                    campus = None
            
                try:
                    course = Course.query.filter_by(ProfID=faculty.EmployeeID).first()

                except:
                    course = None
            try:
                result = db.engine.execute(f"SELECT COUNT(*) FROM Enrolled_In WHERE CourseID = {course.CourseID}")
                num_of_students = result.fetchall()[0][0]

            except:
                num_of_students = None

        except:
            faculty = None
            staff = None
            department = None
            office = None
            building = None
            campus = None
            course = None
            num_of_students = None

        return render_template('contact_employee.html', title=str(contact.FName)+"_"+str(contact.LName), num_of_students=num_of_students, contact=contact, course=course, employee=employee, campus=campus, department=department, office=office, building=building, now=datetime.utcnow())

    elif contact.UserType == 'Student':

        student = Student.query.filter_by(PersonID=contact.PersonID).first()

        # All of this error catching is to avoid any possible problems causing the site to crash
        try:
            if student.StudentType == "Undergrad":

                try:
                    enrolled_in = Enrolled_In.query.filter_by(StudentID=student.StudentID).first()

                except:
                    enrolled_in = None

                try:
                    course = Course.query.filter_by(CourseID=enrolled_in.CourseID).first()

                except:
                    course = None
                
            elif student.StudentType == "Graduate":

                try:
                    registered_for = Registered_For.query.filter_by(StudentID=student.StudentID).first()

                except:
                    registered_for = None

                try:
                    course = Course.query.filter_by(CourseID=registered_for.CourseID).first()

                except:
                    course = None

            try:
                result = db.engine.execute(f"SELECT COUNT(*) FROM Enrolled_In WHERE CourseID = {course.CourseID}")
                num_of_students = result.fetchall()[0][0]

            except:
                num_of_students = None
        
        except:
            enrolled_in = None
            course = None
            registered_for = None
            num_of_students = None

        return render_template('contact_student.html', title=str(contact.FName)+"_"+str(contact.LName), num_of_students=num_of_students, contact=contact, course=course, student=student, now=datetime.utcnow())

@app.route("/result", methods=['GET', 'POST'])
def result():
    form = SearchForm()
    return render_template('result.html', title='Result', form=form)

@app.route("/admin", methods=['GET', 'POST'])
def admin():
    # i think i need to send all of the content to the page because otherwise I will need to keep resending stuff
    persons = Person.query.all()
    return render_template('admin.html', title='Admin', people= persons)

@app.route("/admin/manage", methods=['GET', 'POST'])
def manage():
    if request.method == 'GET':
        model = request.args.get("model")
        
        data = getModel(model)
        # results =  []
        
        
        return jsonify(data)
    return "test"

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
        contact = Person(FName=form.FName.data, LName=form.LName.data, Email=form.Email.data, PhoneNum=form.PhoneNum.data, UserType='Employee', Manager=form.Manager.data)
        db.session.add(contact)
        db.session.commit()
        flash('You have added a new contact!', 'success')
        return redirect(url_for('home'))
    return render_template('createcontact.html', title='New Contact',
                           form=form, legend='New Contact')

@app.route("/contact/newstudent", methods=['GET', 'POST'])
@login_required                           
def new_student():

    # only allow those who are marked as managers, our version of admins, to add new people
    current_contact = Person.query.filter_by(Email=current_user._get_current_object().email).first()

    if current_contact == None:

        flash('You are not allowed to add a new entry', 'danger')
        return redirect(url_for('home'))

    elif current_contact.Manager == 0:
        
        flash('You are not allowed to add a new entry', 'danger')
        return redirect(url_for('home'))

    form = StudentForm()
    if form.validate_on_submit():
        contact = Person(FName=form.FName.data, LName=form.LName.data, Email=form.Email.data, PhoneNum=form.PhoneNum.data, UserType="Student", Manager=0)
        db.session.add(contact)
        db.session.commit()
        
        current_add = Person.query.filter_by(Email=form.Email.data).first()
        student = Student(PersonID=current_add.PersonID, EnrollmentStatus=form.EnrollmentStatus.data, CreditHoursTotal='0', StudentType=form.StudentType.data)
        db.session.add(student)
        db.session.commit()
        flash('You have added a new contact!', 'success')
        return redirect(url_for('home'))
    return render_template('createstudent.html', title='New Student',
                           form=form, legend='New Student')
                           
@app.route("/contact/newemployee", methods=['GET', 'POST'])
@login_required                               
def new_employee():

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
        contact = Person(FName=form.FName.data, LName=form.LName.data, Email=form.Email.data, PhoneNum=form.PhoneNum.data, UserType="Employee", Manager=form.Manager.data)
        db.session.add(contact)
        db.session.commit()
        
        current_emp = Person.query.filter_by(Email=form.Email.data).first()        
        employee = Employee(ManagerID=form.ManagerID.data, PersonID=current_emp.PersonID, EmployeeType=form.EmployeeType.data) #set managerID to 10 for testing 
        db.session.add(employee)
        db.session.commit()
        flash('You have added a new contact!', 'success')
        return redirect(url_for('home'))
    return render_template('createcontact.html', title='New Employee',
                           form=form, legend='New Employee')

                           
@app.route("/contact/select", methods=['GET', 'POST'])
@login_required                          
def selectaddcontact(): 
    return render_template('selectaddcontact.html', title='Add Select', legend='Add Select') 

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
        contact.UserType = contact.UserType
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

def getModel(model):
    session = db.session

    if (model == "Employee"):

        items = session.query(Person,Employee).filter(Person.PersonID == Employee.PersonID).all()
        # employees = Employee.query.join(Person, Employee.PersonID == Person.PersonID).all()
        results = []
        for item in items:
            person = item.Person.serialize()
            employee = item.Employee.serialize()
            Merge(person,employee)
            print(person)
            results.append(person)
        return results
    elif (model == "All"):
        persons = Person.query.all()
        results = []
        for person in persons:
            results.append(person.serialize())
        return results
    elif (model == "Student"):
        items = session.query(Student,Person).filter(Person.PersonID == Student.PersonID).all()
        results = []
        for item in items:
            person = item.Person.serialize()
            student = item.Student.serialize()
            Merge(person,student)
            print(person)
            results.append(person)
        return results
    elif (model == "Campus"):
        items = Campus.query.all()
        results = []
        for item in items:
            campus = item.serialize()
            results.append(campus)
        return results
    elif (model == "Building"):
        items = session.query(Building, Campus).filter(Building.CampusID== Campus.CampusID).all()
        results = []
        for item in items:
            campus = item.Campus.serialize()
            building = item.Building.serialize()
            Merge(campus, building)
            results.append(campus)
        return results
    elif (model == "Department"):
        results = []
        items = session.query(Building, Department).filter(Department.BuildingID == Building.BuildingID).all()
        for item in items:
            department = item.Department.serialize()
            building = item.Building.serialize()
            Merge(building, department)
            results.append(building)
        return results
    elif (model == "Office"):
        results = []
        items = session.query(Building, Office).filter(Office.BuildingID == Building.BuildingID).all()
        for item in items:
            office = item.Office.serialize()
            building = item.Building.serialize()
            Merge(building, office)
            results.append(building)
        return results
    elif (model == "Faculty"):
        results = []
        items = session.query(Faculty, Employee, Person).filter(Employee.EmployeeID == Faculty.EmployeeID).filter(Employee.PersonID == Person.PersonID).all()
        for item in items:
            faculty = item.Faculty.serialize()
            employee = item.Employee.serialize()
            person   = item.Person.serialize()
            Merge(faculty, employee)
            Merge(faculty,person)
            results.append(faculty)
        return results
    elif (model == "Course"):
        results = []
        return results
    elif (model == "Prereqs"):
        results = []
        return results
    elif (model == "Undergrad"):
        results = []
        return results
    elif (model == "Enrolled_In"):
        results = []
        return results
    elif (model == "Graduate"):
        results = []
        return results
    elif (model == "Registered_For"):
        results = []
        return results
    elif (model == "Teaching_Assistant"):
        results = []
        return results
    elif (model == "Research_Assistant"):
        results = []
        return results
    elif (model == "Alumni"):
        results = []
        return results
    elif (model == "Retiree"):
        results = []
        return results
    elif (model == "Staff"):
        results = []
        return results
    
    return None

def Merge(dict1, dict2):
    return (dict1.update(dict2))