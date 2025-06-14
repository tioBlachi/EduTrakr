"""
Database Logic Module

Manages all database operations including user creation, authentication,
and schema setup.
"""

import sqlite3 as sq3
import hashlib

DB_NAME = 'edutrakr.db'

# --- Helpers ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_connection():
    return sq3.connect(DB_NAME)

def get_user_name(email, role):
    conn = get_connection()
    cur = conn.cursor()

    if role == "student":
        query = """
            SELECT s.name
            FROM users u
            JOIN students s ON u.id = s.user_id
            WHERE u.email = ?
        """
    elif role == "instructor":
        query = """
            SELECT i.name
            FROM users u
            JOIN instructors i ON u.id = i.user_id
            WHERE u.email = ?
        """
    else:
        return None

    cur.execute(query, (email,))
    result = cur.fetchone()
    conn.close()
    return result[0] if result else None


# --- User Management ---
def create_user(email, password, role, name):
    role = role.lower()
    hashed_password = hash_password(password)
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Insert into users table
        cur.execute(
            "INSERT INTO users (email, password, role) VALUES (?, ?, ?)",
            (email, hashed_password, role)
        )
        user_id = cur.lastrowid

        # Add to role-specific table
        if role == 'student':
            cur.execute("INSERT INTO students (user_id, name) VALUES (?, ?)", (user_id, name))
        elif role == 'instructor':
            cur.execute("INSERT INTO instructors (user_id, name) VALUES (?, ?)", (user_id, name))

        conn.commit()
        return True
    except sq3.IntegrityError:
        return False
    finally:
        conn.close()

def authenticate_user(email, password):
    hashed_password = hash_password(password)
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT role FROM users WHERE email = ? AND password = ?",
        (email, hashed_password)
    )
    result = cur.fetchone()
    conn.close()
    return result[0] if result else None

# --- Table Setup ---
def initialize_database():
    print("Initializing database...")
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT CHECK(role IN ('student', 'instructor')) NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            user_id INTEGER PRIMARY KEY,
            name TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS instructors (
            user_id INTEGER PRIMARY KEY,
            name TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_database()
