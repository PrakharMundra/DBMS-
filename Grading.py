import tkinter as tk
from functools import partial
from tkinter import *
from tkinter import simpledialog
from tkinter import ttk
from tkinter import messagebox
import pyaes
import base64
import mysql.connector
import uuid


username = ""

#change the user and password here
db=mysql.connector.connect(
    host="localhost",
    user="root",
    password="mySQLdbms712",
)

cursor=db.cursor()
create_db="""CREATE DATABASE IF NOT EXISTS grading"""
cursor.execute(create_db)
cursor.execute("use grading")
# cursor.execute("""CREATE TABLE IF NOT EXISTS secretKey(id INTEGER PRIMARY KEY, skey TEXT NOT NULL)""")
# cursor.execute("SELECT * FROM secretKey")
# temp=cursor.fetchall()
# if (temp):
#     key = temp[0][1]
# else:
#     key = uuid.uuid4().hex  
#     insert_key = """INSERT INTO secretKey (id,skey) VALUES (1,%s)"""
#     cursor.execute(insert_key, [key])
#     db.commit()
cursor.execute("""
CREATE TABLE IF NOT EXISTS Teacher
(
  teacher_id INT NOT NULL,
  name VARCHAR(30) NOT NULL,
  PRIMARY KEY (teacher_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Class
(
  Name VARCHAR(30) NOT NULL,
  ID INT NOT NULL,
  teacher_id INT NOT NULL,
  PRIMARY KEY (ID),
  FOREIGN KEY (teacher_id) REFERENCES Teacher(teacher_id)  ON
DELETE CASCADE
)
""")
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS User
# (
#   Role VARCHAR(30) NOT NULL
# )
# """)
cursor.execute("""
CREATE TABLE IF NOT EXISTS Teacher_phone_number
(
  phone_number INT NOT NULL ,
  teacher_id INT NOT NULL,
  PRIMARY KEY (phone_number, teacher_id),
  FOREIGN KEY (teacher_id) REFERENCES Teacher(teacher_id) ON DELETE CASCADE
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS Student
(
  stud_id INT NOT NULL,
  name VARCHAR(30) NOT NULL,
  year INT NOT NULL,
  ID INT NOT NULL,
  PRIMARY KEY (stud_id),
  FOREIGN KEY (ID) REFERENCES Class(ID) ON DELETE CASCADE
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS Course
(
  Course_id INT NOT NULL,
  name VARCHAR(30) NOT NULL,
  credits INT NOT NULL,
  course_total INT NOT NULL,
  teacher_id INT,
  PRIMARY KEY (Course_id),
  FOREIGN KEY (teacher_id) REFERENCES Teacher(teacher_id)  ON DELETE CASCADE
)
""")
cursor.execute(""" 
CREATE TABLE IF NOT EXISTS Student_phone_number 
(
  phone_number INT NOT NULL,
  stud_id INT NOT NULL,
  PRIMARY KEY (phone_number, stud_id),
  FOREIGN KEY (stud_id) REFERENCES Student(stud_id)  ON DELETE CASCADE
)
""")
cursor.execute("""
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
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS Reports
(
  CG FLOAT CHECK(CG >= 2.0 AND CG <= 10.0),
  Area_for_improvement VARCHAR(30) ,
  Goals VARCHAR(30),
  stud_id INT NOT NULL,
  PRIMARY KEY (stud_id),
  FOREIGN KEY (stud_id) REFERENCES Student(stud_id)  ON DELETE CASCADE
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS Takes
(
  Grade VARCHAR(2) ,
  stud_id INT NOT NULL,
  Course_id INT NOT NULL,
  PRIMARY KEY (stud_id, Course_id),
  FOREIGN KEY (stud_id) REFERENCES Student(stud_id),
  FOREIGN KEY (Course_id) REFERENCES Course(Course_id)  ON DELETE CASCADE
)
""")

##add a new course to the database

# cursor.execute("INSERT INTO Course (Course_id, name, credits, course_total, teacher_id) VALUES (1, 'Maths', 3, 100, 1)")
# cursor.execute("INSERT INTO Course (Course_id, name, credits, course_total, teacher_id) VALUES (2, 'Science', 4, 120, 2)")
# cursor.execute("INSERT INTO Course (Course_id, name, credits, course_total, teacher_id) VALUES (3, 'History', 2, 80, 3)")
# cursor.execute("INSERT INTO Course (Course_id, name, credits, course_total, teacher_id) VALUES (4, 'English', 3, 90, 1)")
# db.commit()
# cursor.execute("INSERT INTO Course (Course_id, name, credits, course_total, teacher_id) VALUES (5, 'Programming', 5, 150, 4)")


# # # Add a new teacher to the database
# cursor.execute("INSERT INTO Teacher (teacher_id,name) VALUES (1,'Ms. Smith')")
# cursor.execute("INSERT INTO Teacher (teacher_id,name) VALUES (2,'Mr. Johnson')")
# cursor.execute("INSERT INTO Teacher (teacher_id,name) VALUES (3,'Dr. Lee')")

# # Add a new class to the database
# cursor.execute("INSERT INTO Class (ID,name, teacher_id) VALUES (1,'CS', 1)")
# cursor.execute("INSERT INTO Class (ID,name, teacher_id) VALUES (2,'Math', 2)")
# cursor.execute("INSERT INTO Class (ID,name, teacher_id) VALUES (3,'Electrical', 3)")

window = Tk()
window.update()
window.configure(bg='#292841')
window.title("Grading Management System")


def student_login():
    global username
    global name
    username = student_id_entry.get() 
    name = student_name_entry.get()
    # query to check if student exists
    query = "SELECT stud_id, name FROM Student WHERE stud_id=%s AND name=%s;"
    cursor.execute(query, (username, name))
    result = cursor.fetchone()
    print(result)
    if result == None:
        # if student does not exist
        tk.messagebox.showerror("Error", "Invalid id or name")
    else:
        # if student exists
        tk.messagebox.showinfo("Welcome", "Login successful")
        open_student_details_window(username)

        student_window.destroy()


def teacher_login():
    global username
    global name
    username = teacher_id_entry.get()
    name = teacher_name_entry.get()
    query = "SELECT teacher_id, name FROM Teacher WHERE teacher_id=%s AND name=%s;"
    cursor.execute(query, (username, name))
    result = cursor.fetchone()
    print(result)
    if result == None:
        tk.messagebox.showerror("Error", "Invalid id or name")
    else:
        tk.messagebox.showinfo("Welcome", "Login successful")
        print(name)
        grade_input(name)
def grade_input(name):
    # Create tkinter window
    print(name)
    grade_window = tk.Toplevel()
    grade_window.title("Add Grade")
    grade_window.geometry("400x500")
    grade_window.configure(bg='#292841')
    # Create tkinter widgets
    teacher_name_label = tk.Label(grade_window, text=f"Teacher: {name}")
    course_label = tk.Label(grade_window, text="Course ID:")
    course_entry = tk.Entry(grade_window)
    student_id_label = tk.Label(grade_window, text="Student ID:")
    student_id_entry = tk.Entry(grade_window)
    grade_label = tk.Label(grade_window, text="Grade:")
    grade_entry = tk.Entry(grade_window)
    add_button = tk.Button(grade_window, text="Add Grade", command=lambda: add_grade(course_entry.get(), student_id_entry.get(), grade_entry.get()))

    # Place tkinter widgets on window
    teacher_name_label.pack()
    course_label.pack()
    course_entry.pack()
    student_id_label.pack()
    student_id_entry.pack()
    grade_label.pack()
    grade_entry.pack()
    add_button.pack()

def add_grade(course_id, student_id, grade):
    # Check if course and student exist in database
    query = "SELECT * FROM Takes WHERE stud_id=%s AND Course_id=%s;"
    cursor.execute(query, (student_id, course_id))
    result = cursor.fetchone()
    if result == None:
        tk.messagebox.showerror("Error", "Invalid course or student ID")
    else:
        # Update student's grade in the Takes table
        query = "UPDATE Takes SET Grade=%s WHERE stud_id=%s AND Course_id=%s;"
        cursor.execute(query, (grade, student_id, course_id))
        db.commit()
        tk.messagebox.showinfo("Success", "Grade added")

def open_student_details_window(username):
    # create a new window to display student details
    student_details_window = tk.Toplevel()
    student_details_window.title("Student Details")
    student_details_window.geometry("400x500")
    # student_details_window = tk.Toplevel(window)
    
    # window.geometry("800x600")
    
    student_details_window.configure(bg='#292841')

    # query to get the details of the logged in student
    query = "SELECT * FROM Student WHERE stud_id=%s AND name=%s;"
    cursor.execute(query, (username, name))
    student_data = cursor.fetchone()

    # get phone number from database
    query = "SELECT phone_number FROM Student_phone_number WHERE stud_id = %s"
    cursor.execute(query, (username,))
    phone_numbers = cursor.fetchall()

    # display the student details
    tk.Label(student_details_window, text=f"ID: {student_data[0]}", bg='#292841', fg='white').grid(row=0, column=0, padx=10, pady=5)
    tk.Label(student_details_window, text=f"Name: {student_data[1]}", bg='#292841', fg='white').grid(row=1, column=0, padx=10, pady=5)
    tk.Label(student_details_window, text=f"Year: {student_data[2]}", bg='#292841', fg='white').grid(row=2, column=0, padx=10, pady=5)
    row_counter=3
    if phone_numbers:
       for i, phone_number in enumerate(phone_numbers):
        row_counter+=1
        tk.Label(student_details_window, text=f"Phone Number {i+1}: {phone_number[0]}", bg='#292841', fg='white').grid(row=i+3, column=0, padx=10, pady=5)
    else:
       tk.Label(student_details_window, text="Phone Number: Not updated", bg='#292841', fg='white').grid(row=3, column=0, padx=10, pady=5)
       row_counter+=1 
    add_phone_number_button = tk.Button(student_details_window, text="Add Phone Number", command=open_add_phone_number_window)
    add_phone_number_button.grid(row=row_counter, column=0, padx=10, pady=5)
    row_counter+=1

    query = f"SELECT c.name, t.Grade FROM Takes t JOIN Course c ON t.Course_id = c.Course_id WHERE t.stud_id = '{username}';"
    cursor.execute(query)
    courses = cursor.fetchall()
    print(courses)
    if courses:
        tk.Label(student_details_window, text="Courses Taken:", bg='#292841', fg='white').grid(row=row_counter, column=0, padx=10, pady=5)
        for i, course in enumerate(courses):
            tk.Label(student_details_window, text=f"{i+1}. {course[0]} - Grade: {course[1]}", bg='#292841', fg='white').grid(row=row_counter+i+1, column=0, padx=10, pady=5)
            row_counter+=1
    else:
        tk.Label(student_details_window, text="No courses taken", bg='#292841', fg='white').grid(row=row_counter, column=0, padx=10, pady=5)
        row_counter+=1


    add_course_button = tk.Button(student_details_window, text="Add Course", command=open_course_selection)
    add_course_button.grid(row=row_counter+5, column=0, padx=10, pady=10)
    row_counter+=1


def open_add_phone_number_window():
    # create a new window to add phone number   
    add_phone_number_window = tk.Toplevel(window)
    add_phone_number_window.title("Add Phone Number")
    add_phone_number_window.configure(bg='#292841')

    # label and entry widget for phone number
    tk.Label(add_phone_number_window, text="Phone Number:", bg='#292841', fg='white').grid(row=0, column=0, padx=10, pady=5)
    phone_number_entry = tk.Entry(add_phone_number_window, bg='#44475a', fg='white')
    phone_number_entry.grid(row=0, column=1, padx=10, pady=5)

    # button to add phone number
    add_phone_number_button = tk.Button(add_phone_number_window, text="Add", bg='#44475a', fg='white', command=lambda: add_phone_number(phone_number_entry.get()))
    add_phone_number_button.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

def add_phone_number(phone_number):
    # insert the phone number into the database
    query = "INSERT INTO Student_phone_number (phone_number, stud_id) VALUES (%s, %s);"
    cursor.execute(query, (phone_number, username))
    db.commit()
    tk.messagebox.showinfo("Success", "Phone number added successfully")
    add_phone_number.destroy()


def open_course_selection():
    # create a new window to display course selection
    course_selection_window = tk.Toplevel()
    course_selection_window.title("Course Selection")
    course_selection_window.geometry("400x500")

    
    # query to get all available courses
    course_selection_window.configure(bg='#292841')

    query = "SELECT Course_id, name FROM Course"
    cursor.execute(query)
    courses = cursor.fetchall()

    # create a list of course names to display in the dropdown
    course_names = [f"{course[0]} - {course[1]}" for course in courses]

    # create a StringVar to store the selected course
    selected_course = tk.StringVar()

    # create a dropdown to select the course
    course_dropdown = tk.OptionMenu(course_selection_window, selected_course, *course_names)
    course_dropdown.configure(bg='#333333', fg='white', width=20)
    course_dropdown.grid(row=0, column=0, padx=10, pady=5)

    # create a button to save the selected course
    def save_course():
        # get the course_id from the selected option
        course_id = int(selected_course.get().split(" - ")[0])

        # query to add the course to the Takes table
        query = "INSERT INTO Takes (Grade, stud_id, Course_id) VALUES ('na', %s, %s)"
        try:
            cursor.execute(query, (username, course_id))
            db.commit()
            messagebox.showinfo("Success", "Course selection successful!")
        except:
            db.rollback()
            messagebox.showerror("Error", "Course selection unsuccessful.")
    
    save_button = tk.Button(course_selection_window, text="Save", bg='#333333', fg='white', command=save_course)
    save_button.grid(row=1, column=0, padx=10, pady=5)


def student_login_page():
    global student_id_entry
    global student_name_entry
    global student_window
    student_window = tk.Tk()
    student_window.title("Student Login")
    student_window.geometry("300x200")
    student_window.configure(bg='#292841')

    student_id_label = tk.Label(student_window, text="Student ID:")
    student_id_label.pack()
    student_id_entry = tk.Entry(student_window)
    student_id_entry.pack()

    student_name_label = tk.Label(student_window, text="Name:")
    student_name_label.pack()
    student_name_entry = tk.Entry(student_window)
    student_name_entry.pack()

    student_login_button = tk.Button(student_window, text="Login", command=student_login)
    student_login_button.pack()

def teacher_login_page():
    global teacher_id_entry
    global teacher_name_entry
    global teacher_window
    teacher_window = tk.Tk()
    teacher_window.title("Teacher Login")
    teacher_window.geometry("300x200")
    teacher_window.configure(bg='#292841')

    teacher_id_label = tk.Label(teacher_window, text="teacher ID:")
    teacher_id_label.pack()
    teacher_id_entry = tk.Entry(teacher_window)
    teacher_id_entry.pack()

    teacher_name_label = tk.Label(teacher_window, text="Name:")
    teacher_name_label.pack()
    teacher_name_entry = tk.Entry(teacher_window)
    teacher_name_entry.pack()

    teacher_login_button = tk.Button(teacher_window, text="Login", command=teacher_login)
    teacher_login_button.pack()
def insert_student(stud_id, name, year, ID):
    cursor = db.cursor()
    sql = "INSERT INTO Student (stud_id, name, year, ID) VALUES (%s, %s, %s, %s)"
    val = (stud_id, name, year, ID)
    cursor.execute(sql, val)
    db.commit()
    print(cursor.rowcount, "record inserted.")
    student_login_page()

def add_student():
    window = Tk()
    window.update()
    window.configure(bg='#292841')
    window.geometry("300x200")
    window.title("Add Student")
    stud_id_label = Label(window, text="Student ID:")
    stud_id_label.pack()
    stud_id_entry = Entry(window)
    stud_id_entry.pack()
    name_label = Label(window, text="Name:")
    name_label.pack()
    name_entry = Entry(window)
    name_entry.pack()
    year_label = Label(window, text="Year:")
    year_label.pack()
    year_entry = Entry(window)
    year_entry.pack()
    ID_label = Label(window, text="Class ID:")
    ID_label.pack()
    ID_entry = Entry(window)
    ID_entry.pack()
    save_button = Button(window, text="Save", command=lambda: insert_student(stud_id_entry.get(), name_entry.get(), year_entry.get(), ID_entry.get()))
    save_button.pack()

def show_details():
    # get the details of the student
    query = "SELECT * FROM Student WHERE stud_id=%s;"
    cursor.execute(query, (username,))
    result = cursor.fetchone()

    # create a new window to show the details
    details_window = tk.Toplevel(window)
    details_window.title("Student Details")
    details_window.configure(bg='#292841')

    # create labels to display the details
    stud_id_label = tk.Label(details_window, text="Student ID: "+str(result[0]), bg='#292841', fg='white')
    name_label = tk.Label(details_window, text="Name: "+result[1], bg='#292841', fg='white')
    year_label = tk.Label(details_window, text="Year: "+str(result[2]), bg='#292841', fg='white')

    # display the labels
    stud_id_label.pack()
    name_label.pack()
    year_label.pack()



def Launch():   
    window.geometry("300x200")
    window.resizable(False, False)
    student_button = Button(window, text="Add Student", command=add_student)
    student_button.pack()
    student_login_button = tk.Button(window, text=" Student Login", command=student_login_page)
    student_login_button.pack()
    teacher_login_button = tk.Button(window, text=" Teacher Login", command=teacher_login_page)
    teacher_login_button.pack()
    query = "SELECT stud_id, name FROM Student "
    cursor.execute(query)
    result = cursor.fetchall()
    print(result)
Launch()
window.mainloop()
   