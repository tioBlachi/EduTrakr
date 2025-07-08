"""
EduTrakr Main App

This is the main Streamlit app that launches the EduTrakr dashboard.
It sets the page configuration and displays the homepage UI elements.
see streamlit docs for more info
"""

import streamlit as st
import utils as util
import database as db
import time

ss = st.session_state

# Page configuration
st.set_page_config(page_title="EduTrakr", page_icon="📚")
st.title("📚 EduTrakr")
st.subheader("Your personal study time tracker")

# need to initialize a new database when rerunning the app for development
# this will also fill the db with fake user data
@st.cache_resource
def init_db():
    db.initialize_database()
    util.generate_db_data()

init_db() 

# Input fields
email = st.text_input("Email")
if not util.is_valid_email(email) and email:
    st.error("Invalid Email Format")

password = st.text_input("Password", type="password")
if len(password) < 6 and password:
    st.error("Password must be at least 6 characters long")

# Login button
login_pressed = st.button("Login")

# Register button (below login)
register_pressed = st.button("Register")

# Actions
if login_pressed:
    st.write(f"Attempting to log in user: `{email}`")
    if login_pressed:
        user = util.check_user_credentials(email, password)
        if user:
            user_id = ss.user_id = user[0]
            name = ss.name = user[1]
            role = ss.role = user[4]
            st.success("Login successful! Redirecting...")
            time.sleep(1.5)
            if role.lower() == 'student':
                st.switch_page("pages/student_dash.py")
            else:
                st.switch_page("pages/instructor_dash.py")
        else:
            st.error("Invalid email or password.")

if register_pressed:
    st.write("Redirecting to registration page...")
    st.switch_page("pages/register.py")

