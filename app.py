
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


# HOME PAGE - DISPLAY AND SEARCH STUDENTS
@app.route("/")
def home():
    connection = sqlite3.connect("students.db")
    cursor = connection.cursor()

    # Search students
    search = request.args.get("search", "")

    cursor.execute("""
        SELECT * FROM students
        WHERE name LIKE ? OR email LIKE ? OR department LIKE ?
    """, ('%' + search + '%', '%' + search + '%', '%' + search + '%'))

    students = cursor.fetchall()

    # Count total students
    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    # Count different departments
    cursor.execute("SELECT COUNT(DISTINCT department) FROM students")
    total_departments = cursor.fetchone()[0]

    # Count different semesters
    cursor.execute("SELECT COUNT(DISTINCT semester) FROM students")
    total_semesters = cursor.fetchone()[0]

    connection.close()

    return render_template(
        "index.html",
        students=students,
        total_students=total_students,
        total_departments=total_departments,
        total_semesters=total_semesters
    )


# ADD STUDENT
@app.route("/add", methods=["POST"])
def add_student():
    name = request.form["name"]
    email = request.form["email"]
    department = request.form["department"]
    semester = request.form["semester"]

    connection = sqlite3.connect("students.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO students
        (name, email, department, semester)
        VALUES (?, ?, ?, ?)
    """, (name, email, department, semester))

    connection.commit()
    connection.close()

    return redirect("/")


# EDIT STUDENT
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_student(id):
    connection = sqlite3.connect("students.db")
    cursor = connection.cursor()

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        department = request.form["department"]
        semester = request.form["semester"]

        cursor.execute("""
            UPDATE students
            SET name=?, email=?, department=?, semester=?
            WHERE id=?
        """, (name, email, department, semester, id))

        connection.commit()
        connection.close()

        return redirect("/")

    cursor.execute("SELECT * FROM students WHERE id=?", (id,))
    student = cursor.fetchone()

    connection.close()

    return render_template("edit.html", student=student)


# DELETE STUDENT
@app.route("/delete/<int:id>")
def delete_student(id):
    connection = sqlite3.connect("students.db")
    cursor = connection.cursor()

    cursor.execute("DELETE FROM students WHERE id=?", (id,))

    connection.commit()
    connection.close()

    return redirect("/")


# RUN APPLICATION
if __name__ == "__main__":
    app.run(debug=True)
