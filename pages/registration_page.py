import streamlit as st
import sqlite3 as sq3
import hashlib

DB_NAME = 'edutrakr.db'

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

# --- Streamlit Registration Page
st.set_page_config(page_title="Register", initial_sidebar_state="collapsed")
st.markdown("""
    <style>
        [data-testid="collapsedControl"] {
            display: none
        }
    </style>
    """, unsafe_allow_html=True)

st.title("Create an Account")

email = st.text_input("Email")
password = st.text_input("Password", type="password")
role = st.selectbox("Select Role", ["Student", "Instructor"])

if st.button("Create Account"):
    if create_user(email, password, role):
        st.success("Account created successfully! Go back to the login page.")
    else:
        st.error("Email already exists.")
