import os
import secrets
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import engine
from flask import render_template, url_for, flash, redirect, request, jsonify
from flask.globals import session
from flaskDemo import app, db, bcrypt
from flaskDemo.models import *
from flaskDemo.forms import RegistrationForm, LoginForm, SearchForm, ContactForm, ContactUpdateForm, StudentForm
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
import json

dbengine: engine
db: SQLAlchemy
dbengine = db.engine
connection = db.engine.connect()




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

            try:
                result = db.engine.execute(f"SELECT COUNT(*) FROM Enrolled_In WHERE CourseID = {course.CourseID}")
                num_of_students = result.fetchall()[0][0]

            except:
                num_of_students = None

        except:
            faculty = None
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
    if not current_user.is_authenticated:
        flash('You are not allowed to go to the manager page', 'danger')
        return redirect(url_for('home'))
    current_contact = Person.query.filter_by(Email=current_user._get_current_object().email).first()
    if current_contact == None:

        flash('You are not allowed to go to the manager page', 'danger')
        return redirect(url_for('home'))

    elif current_contact.Manager == 0:
        
        flash('You are not allowed to go to the manager page', 'danger')
        return redirect(url_for('home'))
    # i think i need to send all of the content to the page because otherwise I will need to keep resending stuff
    persons = Person.query.all()
    return render_template('admin.html', title='Admin', people= persons)

@app.route("/admin/manage", methods=['GET', 'POST'])
@login_required
def manage():
    current_contact = Person.query.filter_by(Email=current_user._get_current_object().email).first()
    if request.method == 'GET':
        if current_contact == None:

            flash('You are not allowed to add a new entry', 'danger')
            return redirect(url_for('home'))

        elif current_contact.Manager == 0:
        
            flash('You are not allowed to add a new entry', 'danger')
            return redirect(url_for('home'))
        model = request.args.get("model")
        
        data = getModel(model)
        # results =  []
       
        return jsonify(data)
    else:
        data = request.get_json()
        result = insertItem(data)
        
        if result:
            return "Added "+ data['model']
        else:
            flash('Failed to add ' + data['model'], 'danger')
            return ""
        return "test"

@app.route("/admin/modelDetails", methods=['GET'])
def getModelDetails():
    if request.method == 'GET':
        data = getModelFields(request.args.get("model")) #this grabs specific details for each model so that the website can adjust the forms
        return data
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
            #print(person)
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
        test = Student.query.all()
        #for item in test:
        #    print(item)
        results = []
        for item in items:
            person = item.Person.serialize()
            student = item.Student.serialize()
            Merge(person,student)
            #print(person)
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
        items = session.query(Course, Prereqs).filter(Course.CourseID == Prereqs.MainCourseID).all()
        results = []
        for item in items:
            course = item.Course.serialize()
            prereqs = item.Prereqs.serialize()
            Merge(course, prereqs)
            results.append(course)
        return results
    elif (model == "Prereqs"):
        cmd = 'SELECT * FROM Prereqs JOIN Course on Prereqs.MainCourseID = Course.CourseID;'
        items = connection.execute(cmd)
        print(items)
        results = convert_to_dict(items)
        
        #results.append(items)
        return results
    elif (model == "Undergrad"):
        cmd = 'SELECT * FROM Undergrad JOIN (SELECT Student.StudentID, Student.PersonID, Student.EnrollmentStatus, Student.CreditHoursTotal, Student.StudentType, Person.FName, Person.LName, Person.Email, Person.PhoneNum FROM Student JOIN Person on Person.PersonID = Student.PersonID) as y on Undergrad.StudentID = y.StudentID'
        items = connection.execute(cmd)
        results = convert_to_dict(items)
        return results
    elif (model == "Enrolled_In"):
        cmd = 'SELECT * FROM Enrolled_In JOIN (SELECT Undergrad.StudentID, Student.PersonID, Student.EnrollmentStatus, Student.CreditHoursTotal, Student.StudentType, Person.FName, Person.LName, Person.Email, Person.PhoneNum FROM Undergrad JOIN Student on Student.StudentID = Undergrad.StudentID JOIN Person on Person.PersonID = Student.PersonID) as y on Enrolled_In.StudentID = y.StudentID'
        items = connection.execute(cmd)
        results = convert_to_dict(items)
        return results
    elif (model == "Graduate"):
        cmd = 'SELECT * FROM Graduate JOIN (SELECT Student.StudentID, Student.PersonID, Student.EnrollmentStatus, Student.CreditHoursTotal, Student.StudentType, Person.FName, Person.LName, Person.Email, Person.PhoneNum FROM Student JOIN Person on Person.PersonID = Student.PersonID) as y on Graduate.StudentID = y.StudentID'
        items = connection.execute(cmd)
        results = convert_to_dict(items)
        return results
    elif (model == "Registered_For"):
        cmd = 'SELECT * FROM Registered_For JOIN (SELECT Graduate.StudentID, Student.PersonID, Student.EnrollmentStatus, Student.CreditHoursTotal, Student.StudentType, Person.FName, Person.LName, Person.Email, Person.PhoneNum FROM Graduate JOIN Student on Student.StudentID = Graduate.StudentID JOIN Person on Person.PersonID = Student.PersonID) as y on Registered_For.StudentID = y.StudentID'
        items = connection.execute(cmd)
        results = convert_to_dict(items)
        return results
    elif (model == "Teaching_Assistant"):
        cmd = 'SELECT * FROM Teaching_Assistant JOIN (SELECT Graduate.StudentID, Student.PersonID, Student.EnrollmentStatus, Student.CreditHoursTotal, Student.StudentType, Person.FName, Person.LName, Person.Email, Person.PhoneNum FROM Graduate JOIN Student on Student.StudentID = Graduate.StudentID JOIN Person on Person.PersonID = Student.PersonID) as y on Teaching_Assistant.StudentID = y.StudentID JOIN Course on Course.CourseID = Teaching_Assistant.CourseID'
        items = connection.execute(cmd)
        results = convert_to_dict(items)
        return results
    elif (model == "Research_Assistant"):
        cmd = 'SELECT * FROM Research_Assistant JOIN (SELECT Graduate.StudentID, Student.PersonID, Student.EnrollmentStatus, Student.CreditHoursTotal, Student.StudentType, Person.FName, Person.LName, Person.Email, Person.PhoneNum FROM Graduate JOIN Student on Student.StudentID = Graduate.StudentID JOIN Person on Person.PersonID = Student.PersonID) as y on Research_Assistant.StudentID = y.StudentID'
        items = connection.execute(cmd)
        results = convert_to_dict(items)
        return results
    elif (model == "Alumni"):
        cmd = 'SELECT * FROM Alumni JOIN (SELECT Student.StudentID, Student.PersonID, Student.EnrollmentStatus, Student.CreditHoursTotal, Student.StudentType, Person.FName, Person.LName, Person.Email, Person.PhoneNum FROM Student JOIN Person on Person.PersonID = Student.PersonID) as y on Alumni.StudentID = y.StudentID'
        items = connection.execute(cmd)
        results = convert_to_dict(items)
        return results
    elif (model == "Retiree"):
        cmd = 'SELECT * FROM Retiree JOIN (Select Employee.EmployeeID, Employee.PersonID, Person.FName, Person.LName, Person.Email, Person.PhoneNum From Employee Join Person on Employee.PersonID = Person.PersonID) as y on y.EmployeeID = Retiree.EmployeeID'
        items = connection.execute(cmd)
        results = convert_to_dict(items)
        return results
    elif (model == "Staff"):
        cmd = 'SELECT * FROM Staff JOIN (Select Employee.EmployeeID, Employee.PersonID, Person.FName, Person.LName, Person.Email, Person.PhoneNum From Employee Join Person on Employee.PersonID = Person.PersonID) as y on y.EmployeeID = Staff.EmployeeID'
        items = connection.execute(cmd)
        results = convert_to_dict(items)
        return results
    elif (model == "User"):
        cmd = 'SELECT user.id, user.username, user.email, Person.FName, Person.LName, Person.PhoneNum FROM user JOIN Person on user.email = Person.email'
        items = connection.execute(cmd)
        results = convert_to_dict(items)
        return results
    elif (model =="Employed Students"):
        text_stmt = db.text("select PersonID, EmployeeID from Employee").columns(
            Employee.PersonID, Employee.EmployeeID)
        qry = session.query(Student).select_entity_from(text_stmt).filter(Student.PersonID == Employee.PersonID)
        items = session.execute(qry).fetchall()
        results = []
        for item in items:
            dict = {"StudentID":item[0], "PersonID": item[1], "EnrollmentStatus": item[2], "CreditHoursTotal": item[3], "StudentType": item[4]}
            results.append(dict)
        return results
    return None


def getModelFields(model):
    item = {}
    
    if (model == "All"):
        item = Person().serialize()
        item.pop('PersonID')
        item['Manager'] = 'bool'
        item['UserType'] = [{'type':'Student'},{'type':'Employee'}]
    elif (model == "Student"):
        item = Student().serialize()
        item['StudentType'] = [{'type':'Undergrad'},{'type':'Graduate'}]

        cmd = 'SELECT Person.PersonID, Person.FName, Person.LName FROM Person;'
        items = connection.execute(cmd)
        
        results = convert_to_dict(items)
        
        item['PersonID'] = convert_to_dict(items)
    elif (model == "Employee"):
        item = Employee().serialize()
        item.pop('EmployeeID')

        cmd = 'SELECT Employee.EmployeeID, Person.FName, Person.LName FROM Employee JOIN Person on Employee.PersonID = Person.PersonID;'
        items = connection.execute(cmd)
        results = convert_to_dict(items)
        results.append({'EmployeeID': None})
        item['ManagerID'] = results

        cmd = 'SELECT Person.PersonID, Person.FName, Person.LName FROM Person;'
        items = connection.execute(cmd)

        item['PersonID'] = convert_to_dict(items)
        item["EmployeeType"] = [{'type':'Staff'}, {'type':'Faculty'},{'type':'Retiree'}]
    elif (model == "Campus"):
        item = Campus().serialize()
        item.pop("CampusID")
    elif (model == "Building"):
        item = Building().serialize()
        item.pop("BuildingID")
        cmd = 'SELECT Campus.CampusID, Campus.CampusName FROM Campus;'
        items = connection.execute(cmd)
        
        item['CampusID'] = convert_to_dict(items)
    elif (model == "Department"):
        item = Department().serialize()
        item.pop("DepartmentID")
        cmd = 'SELECT Building.BuildingID, Building.BuildingName FROM Building;'
        items = connection.execute(cmd)
        
        item['BuildingID'] = convert_to_dict(items)

    elif (model == "Office"):
        item = Office().serialize()
        item.pop('OfficeID')
        cmd = 'SELECT Building.BuildingID, Building.BuildingName FROM Building;'
        items = connection.execute(cmd)
        results = convert_to_dict(items)
        item['BuildingID'] = results
    elif (model == "Faculty"):
        item = Faculty().serialize()
        cmd = 'SELECT Employee.EmployeeID, Person.FName, Person.LName FROM Employee JOIN Person on Employee.PersonID = Person.PersonID;'
        items = connection.execute(cmd)
        item['EmployeeID'] = convert_to_dict(items)
        
        cmd = 'SELECT Office.OfficeID, Building.BuildingName FROM Office JOIN Building on Building.BuildingID = Office.BuildingID;'
        items = connection.execute(cmd)
        results = convert_to_dict(items)
        results.append({'OfficeID': None})
        item["OfficeID"] = results

        cmd = 'SELECT Department.DepartmentID, Department.DepartmentName FROM Department;'
        items = connection.execute(cmd)
        item['DepartmentID'] = convert_to_dict(items)
    elif (model == "Course"):
        item = Course().serialize()
        item.pop("CourseID")
        cmd = 'SELECT Employee.EmployeeID, Person.FName, Person.LName FROM Employee JOIN Person on Employee.PersonID = Person.PersonID;'
        items = connection.execute(cmd)
        item['ProfID'] = convert_to_dict(items)
    elif (model == "Prereqs"):
        item = Prereqs().serialize()
        cmd = 'SELECT Course.CourseDescription, Course.CourseID, Course.CourseName FROM Course;' #we need to add courseName to course
        items = connection.execute(cmd)
        item['MainCourseID'] = convert_to_dict(items)
        items = connection.execute(cmd)
        item['PrereqID'] = convert_to_dict(items)
    elif (model == "Undergrad"):
        item = Undergrad().serialize()
        cmd = 'SELECT Student.StudentID, Person.FName, Person.LName FROM Student JOIN Person on Student.PersonID = Person.PersonID;'
        items = connection.execute(cmd)
        item['StudentID'] = convert_to_dict(items)
    elif (model == "Enrolled_In"):
        item = Enrolled_In().serialize()
        cmd = 'SELECT Undergrad.StudentID, Person.FName, Person.LName FROM Undergrad JOIN Student on Student.StudentID = Undergrad.StudentID JOIN Person on Student.PersonID = Person.PersonID;'
        items = connection.execute(cmd)
        item['StudentID'] = convert_to_dict(items)
        cmd = 'SELECT Course.CourseDescription, Course.CourseID, Course.CourseName FROM Course;' #we need to add courseName to course
        items = connection.execute(cmd)
        item['CourseID'] = convert_to_dict(items)
    elif (model == "Graduate"):
        item = Graduate().serialize()
        cmd = 'SELECT Student.StudentID, Person.FName, Person.LName FROM Student JOIN Person on Student.PersonID = Person.PersonID;'
        items = connection.execute(cmd)
        item['StudentID'] = convert_to_dict(items)
    elif (model == "Registered_For"):
        item = Registered_For().serialize()
        cmd = 'SELECT Graduate.StudentID, Person.FName, Person.LName FROM Graduate JOIN Student on Student.StudentID = Graduate.StudentID JOIN Person on Student.PersonID = Person.PersonID;'
        items = connection.execute(cmd)
        item['StudentID'] = convert_to_dict(items)
        cmd = 'SELECT Course.CourseDescription, Course.CourseID, Course.CourseName FROM Course;' #we need to add courseName to course
        items = connection.execute(cmd)
        item['CourseID'] = convert_to_dict(items)
    elif (model == "Teaching_Assistant"):
        item = Teaching_Assistant().serialize()
        cmd = 'SELECT Graduate.StudentID, Person.FName, Person.LName FROM Graduate JOIN Student on Student.StudentID = Graduate.StudentID JOIN Person on Student.PersonID = Person.PersonID;'
        items = connection.execute(cmd)
        item['StudentID'] = convert_to_dict(items)
        cmd = 'SELECT Course.CourseDescription, Course.CourseID, Course.CourseName FROM Course;' #we need to add courseName to course
        items = connection.execute(cmd)
        item['CourseID'] = convert_to_dict(items)
    elif (model == "Research_Assistant"):
        item = Research_Assistant().serialize()
        cmd = 'SELECT Graduate.StudentID, Person.FName, Person.LName FROM Graduate JOIN Student on Student.StudentID = Graduate.StudentID JOIN Person on Student.PersonID = Person.PersonID;'
        items = connection.execute(cmd)
        item['StudentID'] = convert_to_dict(items)
    elif (model == "Alumni"):
        item = Alumni().serialize()
        cmd = 'SELECT Student.StudentID, Person.FName, Person.LName FROM Student JOIN Person on Student.PersonID = Person.PersonID;'
        items = connection.execute(cmd)
        item['StudentID'] = convert_to_dict(items)
    elif (model == "Retiree"):
        item = Retiree().serialize()
        cmd = 'SELECT Employee.EmployeeID, Person.FName, Person.LName FROM Employee JOIN Person on Employee.PersonID = Person.PersonID;'
        items = connection.execute(cmd)
        item['EmployeeID'] = convert_to_dict(items)
    elif (model == "Staff"):
        item = Staff().serialize()
        cmd = 'SELECT Employee.EmployeeID, Person.FName, Person.LName FROM Employee JOIN Person on Employee.PersonID = Person.PersonID;'
        items = connection.execute(cmd)
        item['EmployeeID'] = convert_to_dict(items)
        cmd = 'SELECT Office.OfficeID, Building.BuildingName FROM Office JOIN Building on Building.BuildingID = Office.BuildingID;'
        items = connection.execute(cmd)
        results = convert_to_dict(items)
        results.append({'OfficeID': None})
        item["OfficeID"] = results

        cmd = 'SELECT Department.DepartmentID, Department.DepartmentName FROM Department;'
        items = connection.execute(cmd)
        item['DepartmentID'] = convert_to_dict(items)
    elif (model == "User"):
        item = User().serialize()

    return item


def Merge(dict1, dict2):
    return (dict1.update(dict2))

def convert_to_dict(resultproxy):
    d, a = {}, []
    for rowproxy in resultproxy:
        # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
        for column, value in rowproxy.items():
            # build up the dictionary
            d = {**d, **{column: value}}
        a.append(d)
    return a

def insertItem(data):
    print(data)
    if (data['model'] == 'All'):
        item = Person(FName=data['FName'], LName=data['LName'], Email=data['Email'], PhoneNum=data['PhoneNum'], UserType=data['UserType'], Manager=data['Manager'])
    elif (data['model'] == 'User'):
        #not sure if we should have this because they would need to set the password
        return False
    elif (data['model'] == 'Employee'):
        item = Employee(ManagerID = data['ManagerID'], PersonID = data['PersonID'], EmployeeType = ['EmployeeType'])
    elif (data['model'] == 'Student'):
         item = Employee(PersonID = data['PersonID'], EnrollmentStatus = data['EnrollmentStatus'], CreditHoursTotal = data['CreditHoursTotal'], StudentType = data['StudentType'])
    elif (data['model'] == 'Campus'):
        item = Campus(CampusName = data['CampusName'])
    elif (data['model'] == 'Building'):
        item = Building(CampusID = data['CampusID'], BuildingName = data['BuildingName'], BuildingAddress = data['BuildingAddress'])
    elif (data['model'] == 'Department'):
        item = Department(DepartmentName = data['DepartmentName'], BuildingID = data['BuildingID'])
    elif (data['model'] == 'Office'):
        item = Office(BuildingID = data['BuildingID'])
    elif (data['model'] == 'Faculty'):
        item = Faculty(EmployeeID = data['EmployeeID'], OfficeID = ['OfficeID'], DepartmentID = ['DepartmentID'])
    elif (data['model'] == 'Course'):
        item = Course(ProfID = data['ProfID'], CourseDescription = data['CourseDescription'], CourseName = data['CourseName'])
    elif (data['model'] == 'Prereqs'):
        item = Prereqs(MainCourseID = data['MainCourseID'], PrereqID = data['PrereqID'])
    elif (data['model'] == 'Undergrad'):
        item = Undergrad(StudentID = data['StudentID'])
    elif (data['model'] == 'Enrolled_In'):
        item = Enrolled_In(StudentID = data['StudentID'], CourseID = data['CourseID'])
    elif (data['model'] == 'Graduate'):
        item = Graduate(StudentID = data['StudentID'], UGCompDate = data['UGCompDate'], GraduateType = data['GraduateType'])
    elif (data['model'] == 'Registered_For'):
        item = Registered_For(StudentID = data['StudentID'], CourseID = data['CourseID'])
    elif (data['model'] == 'Teaching_Assistant'):
        item = Teaching_Assistant(StudentID = data['StudentID'], CourseID = data['CourseID'])
    elif (data['model'] == 'Research_Assistant'):
        item = Reasearch_Assistant(StudentID = data['StudentID'], ResearchFocus = data['ResearchFocus'])
    elif (data['model'] == 'Alumni'):
        item = Alumni(StudentID = data['StudentID'], GraduationDate = data['GraduationDate'], FinalSemester = data['FinalSemester'])
    elif (data['model'] == 'Retiree'):
        item = Retiree(EmployeeID = data['EmployeeID'], RetirementDate = data['RetirementDate'], RetirementPackage = data['RetirementPackage'])
    elif (data['model'] == 'Staff'):
        item = Staff(EmployeeID = data['EmployeeID'], OfficeID = ['OfficeID'], DepartmentID = ['DepartmentID'])
    try:
        db.session.add(item)
        db.session.commit()
        return True
    except:
        return False
        
    