from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import psycopg2
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
)
""")
conn.commit()


@app.get("/")
def home():
    return {"message": "Student Management API"}


@app.post("/add_student")
def add_student(name: str):

    cursor.execute(
        "INSERT INTO students (name) VALUES (%s)",
        (name,)
    )

    conn.commit()

    return {
        "message": f"{name} added successfully"
    }

@app.get("/students")
def get_students():

    cursor.execute("SELECT * FROM students")

    rows = cursor.fetchall()

    students = []

    for row in rows:
        students.append({
            "id": row[0],
            "name": row[1]
        })

    return {
        "students": students
    }

@app.get("/students/{student_id}")
def get_student(student_id: int):

    cursor.execute(
        "SELECT * FROM students WHERE id=%s",
        (student_id,)
    )

    student = cursor.fetchone()

    if not student:
        return {"error": "Student not found"}

    return {
        "id": student[0],
        "name": student[1]
    }

@app.put("/students/{student_id}")
def update_student(student_id: int, name: str):

    cursor.execute(
        "UPDATE students SET name = %s WHERE id = %s",
        (name, student_id)
    )

    conn.commit()

    return {
        "message": "Student updated"
    }

@app.delete("/students/{student_id}")
def delete_student(student_id: int):

    cursor.execute(
        "DELETE FROM students WHERE id = %s",
        (student_id,)
    )

    conn.commit()

    return {
        "message": "Student deleted"
    }