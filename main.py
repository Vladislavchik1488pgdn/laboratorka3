import sqlite3
import customtkinter as ctk
from tkinter import ttk

conn = sqlite3.connect("university.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    dob TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS enrollments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    course_id INTEGER
)
""")

conn.commit()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("University DB")
app.geometry("950x650")


def refresh_students():
    for i in student_table.get_children():
        student_table.delete(i)

    cursor.execute("SELECT * FROM students")
    for row in cursor.fetchall():
        student_table.insert("", "end", values=row)


def refresh_courses():
    for i in course_table.get_children():
        course_table.delete(i)

    cursor.execute("SELECT * FROM courses")
    for row in cursor.fetchall():
        course_table.insert("", "end", values=row)


def refresh_enrollments():
    for i in enroll_table.get_children():
        enroll_table.delete(i)

    cursor.execute("""
        SELECT enrollments.id, students.name, courses.title
        FROM enrollments
        JOIN students ON students.id = enrollments.student_id
        JOIN courses ON courses.id = enrollments.course_id
    """)

    for row in cursor.fetchall():
        enroll_table.insert("", "end", values=row)


def add_student():
    name = student_name.get()
    dob = student_dob.get()

    cursor.execute("INSERT INTO students (name, dob) VALUES (?, ?)", (name, dob))
    conn.commit()
    refresh_students()

    student_name.delete(0, "end")
    student_dob.delete(0, "end")


def add_course():
    title = course_title.get()

    cursor.execute("INSERT INTO courses (title) VALUES (?)", (title,))
    conn.commit()
    refresh_courses()

    course_title.delete(0, "end")


def add_enrollment():
    sid = student_id.get()
    cid = course_id.get()

    cursor.execute("INSERT INTO enrollments (student_id, course_id) VALUES (?, ?)", (sid, cid))
    conn.commit()
    refresh_enrollments()

    student_id.delete(0, "end")
    course_id.delete(0, "end")


def delete_student():
    selected = student_table.focus()
    if not selected:
        return
    data = student_table.item(selected)["values"]

    cursor.execute("DELETE FROM students WHERE id = ?", (data[0],))
    conn.commit()
    refresh_students()


def delete_course():
    selected = course_table.focus()
    if not selected:
        return
    data = course_table.item(selected)["values"]

    cursor.execute("DELETE FROM courses WHERE id = ?", (data[0],))
    conn.commit()
    refresh_courses()


def delete_enrollment():
    selected = enroll_table.focus()
    if not selected:
        return
    data = enroll_table.item(selected)["values"]

    cursor.execute("DELETE FROM enrollments WHERE id = ?", (data[0],))
    conn.commit()
    refresh_enrollments()


title = ctk.CTkLabel(app, text="UNIVERSITY DB", font=("Arial", 22, "bold"))
title.pack(pady=10)

tabs = ctk.CTkTabview(app)
tabs.pack(fill="both", expand=True)

tab1 = tabs.add("Students")
tab2 = tabs.add("Courses")
tab3 = tabs.add("Enrollments")

student_name = ctk.CTkEntry(tab1, placeholder_text="Student Name")
student_name.pack()

student_dob = ctk.CTkEntry(tab1, placeholder_text="Date of Birth")
student_dob.pack()

ctk.CTkButton(tab1, text="Add Student", command=add_student).pack(pady=5)

student_table = ttk.Treeview(tab1, columns=("ID","Name","DOB"), show="headings")
student_table.heading("ID", text="ID")
student_table.heading("Name", text="Name")
student_table.heading("DOB", text="DOB")
student_table.pack(fill="both", expand=True)

ctk.CTkButton(tab1, text="Delete Selected Student", command=delete_student).pack()


course_title = ctk.CTkEntry(tab2, placeholder_text="Course Title")
course_title.pack()

ctk.CTkButton(tab2, text="Add Course", command=add_course).pack(pady=5)

course_table = ttk.Treeview(tab2, columns=("ID","Title"), show="headings")
course_table.heading("ID", text="ID")
course_table.heading("Title", text="Title")
course_table.pack(fill="both", expand=True)

ctk.CTkButton(tab2, text="Delete Selected Course", command=delete_course).pack()


student_id = ctk.CTkEntry(tab3, placeholder_text="Student ID")
student_id.pack()

course_id = ctk.CTkEntry(tab3, placeholder_text="Course ID")
course_id.pack()

ctk.CTkButton(tab3, text="Enroll Student", command=add_enrollment).pack(pady=5)

enroll_table = ttk.Treeview(tab3, columns=("ID","Student","Course"), show="headings")
enroll_table.heading("ID", text="ID")
enroll_table.heading("Student", text="Student")
enroll_table.heading("Course", text="Course")
enroll_table.pack(fill="both", expand=True)

ctk.CTkButton(tab3, text="Delete Selected Enrollment", command=delete_enrollment).pack()

refresh_students()
refresh_courses()
refresh_enrollments()

app.mainloop()

conn.close()