"""
Database Logic Module (To be implemented)

This file will manage all database-related operations such as reading,
writing, and updating study session data.
"""
import sqlite3 as sq3

print("Running database")

conn = sq3.connect("edutrakr.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               email TEXT UNIQUE NOT NULL,
               passowrd TEXT NOT NULL,
               role TEXT CHECK(role IN ('student', 'instructor')) NOT NULL
               )
               """)

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    user_id INTEGER PRIMARY KEY,
    name TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS instructors (
    user_id INTEGER PRIMARY KEY,
    name TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
""")

conn.commit()
conn.close()