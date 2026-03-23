import os
import sqlite3
import mysql.connector

# ---------- AUTO DB SWITCH ----------
USE_SQLITE = os.environ.get("STREAMLIT_SERVER_HEADLESS") == "true"

if USE_SQLITE:
    conn = sqlite3.connect("course_app.db", check_same_thread=False)
    cursor = conn.cursor()
else:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="110307",
        database="course_app"
    )
    cursor = conn.cursor(dictionary=True)

# ---------- FETCH FUNCTION ----------
def dict_fetchall():
    if USE_SQLITE:
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    else:
        return cursor.fetchall()

# ---------- PLACEHOLDER FIX ----------
def q(sql):
    return sql.replace("%s", "?") if USE_SQLITE else sql

# ---------- CREATE TABLES FOR SQLITE ----------
if USE_SQLITE:

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_name TEXT,
        description TEXT,
        price INTEGER,
        seats INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS enrollments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        course_id INTEGER,
        progress INTEGER
    )
    """)

    conn.commit()

# ---------- USERS ----------
def register_user(name, email, password):
    email = email.strip()
    password = password.strip()

    cursor.execute(q("SELECT * FROM users WHERE email=%s"), (email,))
    if cursor.fetchone():
        return False

    cursor.execute(
        q("INSERT INTO users (name, email, password, role) VALUES (%s,%s,%s,%s)"),
        (name, email, password, "student")
    )
    conn.commit()
    return True


def login_user(email, password):
    email = email.strip()
    password = password.strip()

    cursor.execute(
        q("SELECT * FROM users WHERE email=%s AND password=%s"),
        (email, password)
    )
    return cursor.fetchone()


def get_all_students():
    cursor.execute("SELECT id, name, email FROM users WHERE role='student'")
    return dict_fetchall()

# ---------- COURSES ----------
def get_courses():
    cursor.execute("SELECT * FROM courses")
    return dict_fetchall()


def add_course(name, desc, price, seats):
    cursor.execute(
        q("INSERT INTO courses (course_name, description, price, seats) VALUES (%s,%s,%s,%s)"),
        (name, desc, price, seats)
    )
    conn.commit()


def delete_course(course_id):

    cursor.execute(q("DELETE FROM enrollments WHERE course_id=%s"), (course_id,))
    cursor.execute(q("DELETE FROM courses WHERE id=%s"), (course_id,))

    conn.commit()

# ---------- ENROLLMENT ----------
def enroll_course(user_id, course_id):

    cursor.execute(
        q("SELECT * FROM enrollments WHERE user_id=%s AND course_id=%s"),
        (user_id, course_id)
    )

    if not cursor.fetchone():
        cursor.execute(
            q("INSERT INTO enrollments (user_id, course_id, progress) VALUES (%s,%s,%s)"),
            (user_id, course_id, 0)
        )
        conn.commit()


def get_enrollment_details():
    cursor.execute("""
    SELECT 
    u.name,
    u.email,
    c.course_name,
    c.price,
    e.progress
    FROM enrollments e
    JOIN users u ON e.user_id = u.id
    JOIN courses c ON e.course_id = c.id
    """)
    return dict_fetchall()