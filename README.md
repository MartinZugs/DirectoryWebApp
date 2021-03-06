# DirectoryWebApp
Our final web app directory for Comp 453

Change Log: 

11/24 (MZ) 
 - deployed the db and added all of the dummy data
 - added the code to connect to the DB

11/26(EK)
 - Couple of changes with models file to reflect database name changes
 - Played around with basic query for homepage and formatting for user "tiles"
 - Had some issues with nested file for models so created a copy in root directory for now 
 - Added initial Add/Delete functionality at a very basic level. will work to add and expand up soon
 
 11/29(EK)
  -Added initial Update functionality and fixed validation of PersonID on new contact creation

11/30 (PJ)
- cleaned up admin page to work with our layout
- seperated out css and scripts from the html
- redone part of the bootstrap to be a bit nicer
- added a few basic buttons and queries to start seting things up

12/1 (PJ)
- Dropdown with buttons to get the different models from the server
- Setup some of the serverside code for the manage page
- More queries added to serverside
- to send items without redirect to page i need to add a serialize method to each model class
- Table is dynamically filled in when query results come in from the server

12/3(MZ)
Here is what has been added: 
- full login and register functionality
- logic so that those who are non-admins can only edit and delete their own entries and can not add anyone
- logic so that admins can edit, delete, and add as they please
- changing of the person table to add an auto incrementing primary key

12/4 (EK)
- Added Logout function and button to access the Add Contact function
- Added authentication requirement to access logout/add contact
- Split Add Contact form into seperate forms for Employees and Students
- Modified some foreign key constraints on Employee and Student tables to reflect intention of those values. 

12/5 (MZ)
- Added in content on the page when you click on someone's name
- Wrote up all of the connection code so that this data can be pulled together
- Split the contact page into different ones for employee and student and modified the routes.py to work with with that

12/5 (EK)
- Modified Manager Selection option on Employee Add form to be dynamically pulled from Managers on Person Table
-Fixed Bugs: All students were managers and all employees were hard set to Manager '10' ... me :) 

12/5 (PJ)
- fixed a few bugs related to my jquery code
- fixed bootstrap modal
- admin page now requires authentication
- made modal form dynamic so that depending at what you are editing it will have different form inputs
- form is sent through Ajax post to the server so that page doesnt need to be reloaded constantly
- Join subquery for both sql and sqlalchemy
- add methods added to the routes
- Finished the add modal which is fully functional

12/6 (PJ)
- decided to go ham on everything
- fixed error with add by using a flush to get back id of pushed item
- fixed edit modal
- edit modal is now autopoulated from data
- delete is fully functional just needs to be repeated for rest of tables (currently only person for proof of working)
- able to delete multiple entries at once
- creating new way of inputing data into the table because current way only partially works
- edit is almost done
- update is complete just need to pass right ids
- soo turns out some of the inserts were broken, some of our tables were missing auto increment and the others had an issue where 
sqlalchemy will try to create both student and undergrad when inserting undergrad because StudentID is both foreign key and primary key
sqlalchemy.exc.OperationalError: (MySQLdb._exceptions.OperationalError) (1048, "Column 'PersonID' cannot be null")
[SQL: INSERT INTO `Student` (`StudentID`, `PersonID`, `EnrollmentStatus`, `CreditHoursTotal`, `StudentType`) VALUES (%s, %s, %s, %s, %s)]

12/7 (PJ)
- Results for query are now nicely displayed in the table and where things like id go are replaced by the name of the item its refrencing
- added joins to a few of the queries
- code for edit and delete is fully functional
- entries are now updated/ deleted without reloading page
- table header is dynamic
- employed students query works