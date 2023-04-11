-- First we have written the set of sample sql queries as required

create database grading;
use grading;
-- Q1.  Create all the necessary tables, such as student, teacher, course, class, etc.
CREATE TABLE IF NOT EXISTS Teacher
(
  teacher_id INT NOT NULL,
  name VARCHAR(30) NOT NULL,
  PRIMARY KEY (teacher_id)
);

CREATE TABLE IF NOT EXISTS Class
(
  Name VARCHAR(30) NOT NULL,
  ID INT NOT NULL,
  PRIMARY KEY (ID)
);

CREATE TABLE IF NOT EXISTS User
(
  Role VARCHAR(30) NOT NULL
);

CREATE TABLE IF NOT EXISTS Teacher_phone_number
(
  phone_number INT NOT NULL ,
  teacher_id INT NOT NULL,
  PRIMARY KEY (phone_number, teacher_id),
  FOREIGN KEY (teacher_id) REFERENCES Teacher(teacher_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Student
(
  stud_id INT NOT NULL,
  name VARCHAR(30) NOT NULL,
  year INT NOT NULL,
  ID INT NOT NULL,
  PRIMARY KEY (stud_id),
  FOREIGN KEY (ID) REFERENCES Class(ID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Course
(
  Course_id INT NOT NULL,
  name VARCHAR(30) NOT NULL unique,
  credits INT NOT NULL,
  course_total INT NOT NULL,
  teacher_id INT,
  PRIMARY KEY (Course_id),
  FOREIGN KEY (teacher_id) REFERENCES Teacher(teacher_id)  ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Assessment
(
  assess_id INT NOT NULL,
  type VARCHAR(30) NOT NULL,
  total INT NOT NULL,
  date DATE NOT NULL,
  duration FLOAT NOT NULL,
  Course_id INT NOT NULL,
  PRIMARY KEY (assess_id),
  FOREIGN KEY (Course_id) REFERENCES Course(Course_id)  ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Reports
(
  CG FLOAT CHECK(CG >= 2.0 AND CG <= 10.0),
  Area_for_improvement VARCHAR(300) ,
  Goals VARCHAR(300),
  stud_id INT NOT NULL,
  PRIMARY KEY (stud_id),
  FOREIGN KEY (stud_id) REFERENCES Student(stud_id)  ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Takes
(
  Grade VARCHAR(2) ,
  stud_id INT NOT NULL,
  Course_id INT NOT NULL,
  PRIMARY KEY (stud_id, Course_id),
  FOREIGN KEY (stud_id) REFERENCES Student(stud_id),
  FOREIGN KEY (Course_id) REFERENCES Course(Course_id)  ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Student_phone_number 
(
  phone_number INT NOT NULL,
  stud_id INT NOT NULL,
  PRIMARY KEY (phone_number, stud_id),
  FOREIGN KEY (stud_id) REFERENCES Student(stud_id)  ON DELETE CASCADE
);

# # # Add 10 teachesr to the database
INSERT INTO Teacher (teacher_id,name) VALUES (1,'Ms. Sinha');
INSERT INTO Teacher (teacher_id,name) VALUES (2,'Mr. Singh');
INSERT INTO Teacher (teacher_id,name) VALUES (3,'Dr. Sejpal');
INSERT INTO Teacher (teacher_id, name) VALUES (4, 'Mrs. Nayyar');
INSERT INTO Teacher (teacher_id, name) VALUES (5, 'Mr. Khatri');
INSERT INTO Teacher (teacher_id, name) VALUES (6, 'Ms. Sood');
INSERT INTO Teacher (teacher_id, name) VALUES (7, 'Dr. Patel');
INSERT INTO Teacher (teacher_id, name) VALUES (8, 'Mr. Sharma');
INSERT INTO Teacher (teacher_id, name) VALUES (9, 'Ms. Pratap');
INSERT INTO Teacher (teacher_id, name) VALUES (10, 'Mrs. Agarwal');

# # Add 10 classes to the database
INSERT INTO Class (ID,name) VALUES (1,'CS');
INSERT INTO Class (ID,name) VALUES (2,'Math');
INSERT INTO Class (ID,name) VALUES (3,'Electrical');
INSERT INTO Class (ID, name) VALUES (4, 'English');
INSERT INTO Class (ID, name) VALUES (5, 'Science');
INSERT INTO Class (ID, name) VALUES (6, 'History');
INSERT INTO Class (ID, name) VALUES (7, 'Physical Education');
INSERT INTO Class (ID, name) VALUES (8, 'Art');
INSERT INTO Class (ID, name) VALUES (9, 'Music');
INSERT INTO Class (ID, name) VALUES (10, 'Foreign Language');

-- Add new roles for users
INSERT INTO User (Role) VALUES ('Admin');
INSERT INTO User (Role) VALUES ('Student');
INSERT INTO User (Role) VALUES ('Teacher');
INSERT INTO User (Role) VALUES ('Parent');
INSERT INTO User (Role) VALUES ('Guardian');

-- Add phone numbers for teachers
INSERT INTO Teacher_phone_number (phone_number, teacher_id) VALUES (123456789, 1);
INSERT INTO Teacher_phone_number (phone_number, teacher_id) VALUES (234567890, 2);
INSERT INTO Teacher_phone_number (phone_number, teacher_id) VALUES (345678901, 3);
INSERT INTO Teacher_phone_number (phone_number, teacher_id) VALUES (456789012, 4);
INSERT INTO Teacher_phone_number (phone_number, teacher_id) VALUES (567890123, 5);
INSERT INTO Teacher_phone_number (phone_number, teacher_id) VALUES (678901234, 6);
INSERT INTO Teacher_phone_number (phone_number, teacher_id) VALUES (789012345, 7);
INSERT INTO Teacher_phone_number (phone_number, teacher_id) VALUES (890123456, 8);
INSERT INTO Teacher_phone_number (phone_number, teacher_id) VALUES (901234567, 8);
INSERT INTO Teacher_phone_number (phone_number, teacher_id) VALUES (123450987, 10);

-- Insert 10 students
INSERT INTO Student (stud_id, name, year, ID) VALUES (1, 'Aditya', 1, 1);
INSERT INTO Student (stud_id, name, year, ID) VALUES (2, 'Rahul', 4, 2);
INSERT INTO Student (stud_id, name, year, ID) VALUES (3, 'Suhana', 3, 3);
INSERT INTO Student (stud_id, name, year, ID) VALUES (4, 'Nidhi', 1, 4);
INSERT INTO Student (stud_id, name, year, ID) VALUES (5, 'Shahrukh', 1, 5);
INSERT INTO Student (stud_id, name, year, ID) VALUES (6, 'Ishika', 3, 6);
INSERT INTO Student (stud_id, name, year, ID) VALUES (7, 'Rishi', 2, 7);
INSERT INTO Student (stud_id, name, year, ID) VALUES (8, 'Manan', 2, 5);
INSERT INTO Student (stud_id, name, year, ID) VALUES (9, 'Vedant', 2, 6);
INSERT INTO Student (stud_id, name, year, ID) VALUES (10, 'Parth', 4, 7);

-- Insert 10 courses
INSERT INTO Course (Course_id, name, credits, course_total, teacher_id)
VALUES (1, 'Database Systems', 4, 200, 1),
(2, 'Data Structures', 3, 150, 2),
(3, 'Operating Systems', 4, 250, 3),
(4, 'Algorithms', 4, 200, 1),
(5, 'Web Development', 3, 200, 2),
(6, 'Software Engineering', 3, 200, 3),
(7, 'Computer Networks', 4, 250, 1),
(8, 'Programming Languages', 3, 150, 2),
(9, 'Computer Graphics', 4, 250, 3),
(10, 'Artificial Intelligence', 4, 300, 1);

-- Insert 10 Assessments
INSERT INTO Assessment (assess_id, type, total, date, duration, Course_id)
VALUES (1, 'Mid-term Exam', 50, '2022-04-25', 2.5, 1),
(2, 'Final Exam', 100, '2022-06-20', 3.0, 1),
(3, 'Quiz 1', 20, '2022-03-15', 1.0, 2),
(4, 'Quiz 2', 25, '2022-04-05', 1.5, 2),
(5, 'Mid-term Exam', 50, '2022-04-25', 2.5, 3),
(6, 'Final Exam', 100, '2022-06-20', 3.0, 3),
(7, 'Quiz 1', 20, '2022-03-15', 1.0, 4),
(8, 'Quiz 2', 25, '2022-04-05', 1.5, 4),
(9, 'Mid-term Exam', 50, '2022-04-25', 2.5, 5),
(10, 'Final Exam', 100, '2022-06-20', 3.0, 5);

-- Insert reports
INSERT INTO Reports (CG, Area_for_improvement, Goals, stud_id)
VALUES (8.5, 'Improvement in writing skills', 'To improve coding skills', 1),
(7.0, 'Need to improve time management', 'To get better grades', 2),
(9.0, 'Need to improve communication skills', 'To work on team projects', 3),
(6.5, 'Need to improve understanding of concepts', 'To study regularly', 4),
(8.0, 'Need to improve presentation skills', 'To improve problem-solving skills', 5),
(7.5, 'Need to improve analytical skills', 'To learn new technologies', 6),
(9.5, 'Need to improve coding skills', 'To work on open-source projects', 7),
(8.0, 'Need to improve debugging skills', 'To participate in coding competitions', 8),
(7.5, 'Need to improve understanding of algorithms', 'To practice more problems', 9),
(9.0, 'Need to improve team management skills', 'To work on group projects', 10);

INSERT INTO Takes (Grade, stud_id, Course_id) VALUES
('A', 1, 1),
('B', 2, 1),
('C', 3, 1),
('A-', 4, 4),
('B+', 5, 5),
('B', 6, 6),
('A+', 7, 1),
('C-', 8, 8),
('B-', 9, 1),
('A-', 10, 1);

INSERT INTO Student_phone_number (phone_number, stud_id) VALUES
(123457890, 1),
(234568901, 2),
(345689012, 3),
(456890123, 4),
(568901234, 5),
(689012345, 6),
(890123456, 7),
(901234567, 8),
(012345678, 9),
(234567809, 10);


-- The necessary tables have already been created in the SQL code provided, and they are:
-- Teacher
-- Class
-- User
-- Teacher_phone_number
-- Student
-- Course
-- Assessment
-- Reports
-- Takes
-- Student_phone_number

-- Q2.  Insert a new student into the students table.
INSERT INTO Student (stud_id, name, year, ID)
VALUES (11, 'Prakhar Mundra', 2023, 1);
-- This inserts a new student with a student ID of 11, name of Prakhar Mundra, year of 2023, and class ID of 1

-- Q3.  Insert a new teacher into the teachers table.
INSERT INTO Teacher (teacher_id, name)
VALUES (11, 'Dr.Amit Dua');
-- This inserts a new teacher with a teacher ID of 11 and name of Dr.Amit Dua.

-- Q4.  Update a student's information in the students table.
UPDATE Student
SET year = 2024
WHERE stud_id = 11;
-- This updates the year of the student with a student ID of 11 to 2024.

-- Q5.  Delete a teacher from the teachers table.
DELETE FROM Teacher
WHERE teacher_id = 11;
-- This deletes the teacher with a teacher ID of 11.

-- Q6.  Retrieve all the information about a specific student.
SELECT *
FROM Student
WHERE stud_id = 1;
-- This retrieves all the information about the student with a student ID of 1.

-- Q7.  Retrieve the number of students who scored above a certain grade for a specific course for a specific class.
SELECT COUNT(*)
FROM Takes
WHERE Grade > 'B' AND Course_id = 1 AND stud_id IN
(SELECT stud_id FROM Student WHERE ID = 1);
-- This retrieves the number of students who scored above a B in the course with a course ID of 1 and in the class with a class ID of 1

-- 8.  Retrieve the lowest grade for a specific course for a specific class.
SELECT MIN(Grade)
FROM Takes
WHERE Course_id = 1 AND stud_id IN
(SELECT stud_id FROM Student WHERE ID = 1);
-- This retrieves the lowest grade in the course with a course ID of 1 and in the class with a class ID of 1.

-- Q9.  Retrieve the progress of a student.
SELECT Reports.CG, Reports.Area_for_improvement, Reports.Goals
FROM Reports
WHERE stud_id = 1;
-- This retrieves the CG (cumulative grade) of the student with a student ID of 1, as well as their areas for improvement and goals.

-- Q10. Update a student's grade in a course.
UPDATE Takes
SET Grade = 'A'
WHERE stud_id = 1 AND Course_id = 1;
-- This updates the grade of the student with a student ID of 1 in the course with a course ID of 1 to an A.

