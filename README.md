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

12/3(MZ)
Here is what has been added: 
- full login and register functionality
- logic so that those who are non-admins can only edit and delete their own entries and can not add anyone
- logic so that admins can edit, delete, and add as thye please
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