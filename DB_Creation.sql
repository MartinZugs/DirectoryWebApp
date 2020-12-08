DBname:  Team5
user name:  Team5
pwd:  453Team5

USE Team5;

CREATE TABLE `user` (
 `id` int(11) NOT NULL AUTO_INCREMENT,
 `username` varchar(20) NOT NULL,
 `email` varchar(120) NOT NULL,
 `password` varchar(60) NOT NULL,
 PRIMARY KEY (`id`),
 UNIQUE KEY `username` (`username`),
 UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8

CREATE TABLE Person (
    PersonID int NOT NULL AUTO_INCREMENT,
    FName varchar(150),
    LName varchar(150),
    Email varchar(150),
    UserType varchar(20),
    PhoneNum varchar(50),
    Manager BIT,
    CONSTRAINT person_pk PRIMARY KEY (PersonID)
);

CREATE TABLE Student (
    StudentID int NOT NULL AUTO_INCREMENT,
    PersonID int NOT NULL,
    EnrollmentStatus varchar(50),
    CreditHoursTotal int,
    StudentType varchar(30),
    CONSTRAINT student_pk PRIMARY KEY (StudentID),
    FOREIGN KEY (PersonID) REFERENCES Person(PersonID)
);

CREATE TABLE Employee (
    EmployeeID int NOT NULL AUTO_INCREMENT,
    ManagerID int,
    PersonID int NOT NULL,
    EmployeeType varchar(30),
    CONSTRAINT employee_pk PRIMARY KEY (EmployeeID),
    FOREIGN KEY (PersonID) REFERENCES Person(PersonID),
    FOREIGN KEY (ManagerID) REFERENCES Employee(EmployeeID)
);

CREATE TABLE Campus (
    CampusID int NOT NULL AUTO_INCREMENT,
    CampusName varchar(200),
    CONSTRAINT campus_pk PRIMARY KEY (CampusID)
);

CREATE TABLE Building (
    BuildingID int NOT NULL AUTO_INCREMENT,
    CampusID int,
    BuildingName varchar(200),
    BuildingAddress varchar(200),
    CONSTRAINT building_pk PRIMARY KEY (BuildingID),
    FOREIGN KEY (CampusID) REFERENCES Campus(CampusID)
);

CREATE TABLE Department (
    DepartmentID int NOT NULL AUTO_INCREMENT,
    BuildingID int,
    DepartmentName varchar(200),
    CONSTRAINT department_pk PRIMARY KEY (DepartmentID),
    FOREIGN KEY (BuildingID) REFERENCES Building(BuildingID)
);

CREATE TABLE Office (
    OfficeID int NOT NULL AUTO_INCREMENT,
    BuildingID int,
    CONSTRAINT office_pk PRIMARY KEY (OfficeID),
    FOREIGN KEY (BuildingID) REFERENCES Building(BuildingID)
);

CREATE TABLE Faculty (
    EmployeeID int,
    OfficeID int,
    DepartmentID int,
    FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID),
    FOREIGN KEY (OfficeID) REFERENCES Office(OfficeID),
    FOREIGN KEY (DepartmentID) REFERENCES Department(DepartmentID),
    CONSTRAINT faculty_pk PRIMARY KEY (EmployeeID)
);

CREATE TABLE Course (
    CourseID int NOT NULL AUTO_INCREMENT,
    ProfID int,
    CourseDescription varchar(300),
    CourseName varchar(50),
    NoOfSeats int,
    Credits int,
    CONSTRAINT course_pk PRIMARY KEY (CourseID),
    FOREIGN KEY (ProfID) REFERENCES Faculty(EmployeeID)
);

CREATE TABLE Prereqs (
    MainCourseID int,
    PrereqID int,
    FOREIGN KEY (MainCourseID) REFERENCES Course(CourseID),
    FOREIGN KEY (PrereqID) REFERENCES Course(CourseID),
    CONSTRAINT prereq_pk PRIMARY KEY (MainCourseID, PrereqID)
);

CREATE TABLE Undergrad (
    StudentID int,
    FOREIGN KEY (StudentID) REFERENCES Student(StudentID),
    CONSTRAINT undergrad_pk PRIMARY KEY (StudentID)
);

CREATE TABLE Enrolled_In (
    StudentID int,
    CourseID int,
    FOREIGN KEY (StudentID) REFERENCES Undergrad(StudentID),
    FOREIGN KEY (CourseID) REFERENCES Course(CourseID),
    CONSTRAINT enrolled_in_pk PRIMARY KEY (StudentID, CourseID)
);

CREATE TABLE Graduate (
    StudentID int,
    UGCompDate varchar(200),
    GraduateType varchar(200),
    FOREIGN KEY (StudentID) REFERENCES Student(StudentID),
    CONSTRAINT graduate_pk PRIMARY KEY (StudentID)
);

CREATE TABLE Registered_For (
    StudentID int,
    CourseID int,
    FOREIGN KEY (StudentID) REFERENCES Graduate(StudentID),
    FOREIGN KEY (CourseID) REFERENCES Course(CourseID),
    CONSTRAINT registered_for_pk PRIMARY KEY (StudentID, CourseID)
);

CREATE TABLE Teaching_Assistant (
    StudentID int,
    CourseID int,
    FOREIGN KEY (StudentID) REFERENCES Graduate(StudentID),
    FOREIGN KEY (CourseID) REFERENCES Course(CourseID),
    CONSTRAINT ta_pk PRIMARY KEY (StudentID)
);

CREATE TABLE Research_Assistant (
    StudentID int,
    ResearchFocus varchar(200),
    FOREIGN KEY (StudentID) REFERENCES Graduate(StudentID),
    CONSTRAINT ta_pk PRIMARY KEY (StudentID)
);

CREATE TABLE Alumni (
    StudentID int,
    GraduationDate varchar(200),
    FinalSemester varchar(200),
    FOREIGN KEY (StudentID) REFERENCES Student(StudentID),
    CONSTRAINT alumni_pk PRIMARY KEY (StudentID)
);

CREATE TABLE Retiree (
    EmployeeID int,
    RetirementDate varchar(30),
    RetirementPackage varchar(30),
    FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID),
    CONSTRAINT retiree_pk PRIMARY KEY (EmployeeID)
);

CREATE TABLE Staff (
    EmployeeID int,
    OfficeID int,
    DepartmentID int,
    FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID),
    FOREIGN KEY (OfficeID) REFERENCES Office(OfficeID),
    FOREIGN KEY (DepartmentID) REFERENCES Department(DepartmentID),
    CONSTRAINT staff_pk PRIMARY KEY (EmployeeID)
);

INSERT INTO `Person` (`PersonID`, `FName`, `LName`, `Email`, `UserType`, `PhoneNum`, `Manager`) VALUES ('1', 'Frank', 'Zab', 'fzab@gmail.com', 'Employee', '773-983-8902', b'1');
INSERT INTO `Person` (`PersonID`, `FName`, `LName`, `Email`, `UserType`, `PhoneNum`, `Manager`) VALUES ('2', 'Sam', 'Reten', 'sret@gmail.com', 'Student', '364-693-9739', b'0');
INSERT INTO `Student` (`StudentID`, `PersonID`, `EnrollmentStatus`, `CreditHoursTotal`, `StudentType`) VALUES ('1', '2', 'Full-time', '30', 'Undergrad');
INSERT INTO `Undergrad` (`StudentID`) VALUES ('1');
INSERT INTO `Employee` (`EmployeeID`, `ManagerID`, `PersonID`, `EmployeeType`) VALUES ('1', NULL, '1', 'Faculty');
INSERT INTO `Campus` (`CampusID`, `CampusName`) VALUES ('1', 'Lakeshore');
INSERT INTO `Building` (`BuildingID`, `CampusID`, `BuildingName`, `BuildingAddress`) VALUES ('1', '1', 'Cuneo Hall', '6430 N Kenmore Ave, Chicago, IL 60626');
INSERT INTO `Office` (`OfficeID`, `BuildingID`) VALUES ('234', '1');
INSERT INTO `Department` (`DepartmentID`, `BuildingID`, `DepartmentName`) VALUES ('1', '1', 'Computer Science');
INSERT INTO `Faculty` (`EmployeeID`, `OfficeID`, `DepartmentID`) VALUES ('1', '234', '1');
INSERT INTO `Course` (`CourseID`, `ProfID`, `CourseDescription`, `NoOfSeats`, `Credits`) VALUES ('1', '1', 'Database Programming', '20', '3');
INSERT INTO `Enrolled_In` (`StudentID`, `CourseID`) VALUES ('1', '1');
INSERT INTO `Course` (`CourseID`, `ProfID`, `CourseDescription`, `NoOfSeats`, `Credits`) VALUES ('2', '1', 'Algorithms', '25', '3');
INSERT INTO `Person` (`PersonID`, `FName`, `LName`, `Email`, `UserType`, `PhoneNum`, `Manager`) VALUES ('3', 'Alice', 'Drew', 'adrew@gmail.com', 'Employee', '453-867-0922', b'0');
INSERT INTO `Employee` (`EmployeeID`, `ManagerID`, `PersonID`, `EmployeeType`) VALUES ('2', '1', '3', 'Staff');
INSERT INTO `Office` (`OfficeID`, `BuildingID`) VALUES ('142', '1');
INSERT INTO `Staff` (`EmployeeID`, `OfficeID`, `DepartmentID`) VALUES ('2', '142', '1');
INSERT INTO `Prereqs` (`MainCourseID`, `PrereqID`) VALUES ('1', '2');