
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, EmailStr, Field

from database import get_connection

app = FastAPI(title="Student Management API")

app.mount("/static", StaticFiles(directory="static"), name="static")


# Pydantic validation
class Student(BaseModel):
    name: str = Field(min_length=3)
    email: EmailStr
    marks: int = Field(ge=0, le=100)


# Frontend page
@app.get("/")
def home():
    return FileResponse("templates/index.html")


# 1. GET - Display all students
@app.get("/students")
def get_students():

    db = get_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM students ORDER BY id DESC")

    result = cursor.fetchall()

    cursor.close()
    db.close()

    return result


# 2. POST - Add student
@app.post("/students")
def add_student(student: Student):

    db = get_connection()
    cursor = db.cursor()

    query = """
    INSERT INTO students (name, email, marks)
    VALUES (%s, %s, %s)
    """

    values = (
        student.name,
        student.email,
        student.marks
    )

    cursor.execute(query, values)
    db.commit()

    student_id = cursor.lastrowid

    cursor.close()
    db.close()

    return {
        "message": "Student added successfully",
        "student_id": student_id
    }


# GET - Display one student
@app.get("/students/{student_id}")
def get_student(student_id: int):

    db = get_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM students WHERE id = %s",
        (student_id,)
    )

    student = cursor.fetchone()

    cursor.close()
    db.close()

    if student is None:
        raise HTTPException(404, "Student not found")

    return student


# 3. PUT - Update student
@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):

    db = get_connection()
    cursor = db.cursor()

    query = """
    UPDATE students
    SET name = %s, email = %s, marks = %s
    WHERE id = %s
    """

    values = (
        student.name,
        student.email,
        student.marks,
        student_id
    )

    cursor.execute(query, values)
    db.commit()

    updated = cursor.rowcount

    cursor.close()
    db.close()

    if updated == 0:
        # Check whether the student exists but values were unchanged
        db = get_connection()
        cursor = db.cursor()

        cursor.execute(
            "SELECT id FROM students WHERE id = %s",
            (student_id,)
        )

        exists = cursor.fetchone()

        cursor.close()
        db.close()

        if exists is None:
            raise HTTPException(404, "Student not found")

    return {"message": "Student updated successfully"}


# 4. DELETE - Delete student
@app.delete("/students/{student_id}")
def delete_student(student_id: int):

    db = get_connection()
    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id = %s",
        (student_id,)
    )

    db.commit()

    deleted = cursor.rowcount

    cursor.close()
    db.close()

    if deleted == 0:
        raise HTTPException(404, "Student not found")

    return {"message": "Student deleted successfully"}
