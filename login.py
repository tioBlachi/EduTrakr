"""
Authentication Module (To be implemented)

This file will handle user authentication using streamlit-authenticator.
Currently empty, but reserved for login and user management logic.
"""

import streamlit as st
import sqlite3 as sq3
import hashlib

DB_NAME = 'edutrakr.db'

# --- DB Functions
def get_connection():
    return sq3.connect(DB_NAME)

def create_user(email, password, role):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (email, password, role) VALUES (?, ?, ?)", (email, hashed_password, role))
        conn.commit()
        return True
    except sq3.IntegrityError:
        return False
    finally:
        conn.close()

def authenticate_user(email, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT role FROM users WHERE email = ? AND password = ?", (email, hashed_password))
    result = cur.fetchone()
    conn.close()
    return result[0] if result else None

# --- Streamlit Login Page
st.title("Welcome to EduTrakr!")

st.subheader("Login to Your Account")
email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Login"):
    role = authenticate_user(email, password)
    if role:
        st.success(f"Loggen in as {role.capitalize()}")
        st.info(f"Redirect to {role} dashboard here.")
    else:
        st.error("Invalid email or password")

st.divider()

st.write("Create Account")
# new_email = st.text_input("New Email")
# new_password = st.text_input("New Password", type="password")
# role = st.selectbox("Select Role", ["Student", "Instructor"])

if st.button("Register"):
    st.switch_page("pages/registration_page.py")
    # if create_user(new_email, new_password, role):
    #     st.success("Account created successfully! Go to Login")
    # else:
    #     st.error("Email already exists")
