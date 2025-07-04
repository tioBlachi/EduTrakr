"""
EduTrakr Main App

This is the main Streamlit app that launches the EduTrakr dashboard.
It sets the page configuration and displays the homepage UI elements.
see streamlit docs for more info
"""

import streamlit as st
import utils as util
import database as db

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
if not util.is_valid_email(email):
    st.error("Invalid Email Format")

password = st.text_input("Password", type="password")
if len(password) <= 6:
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
            st.success("Login successful!")
            st.write(f"Welcome back!")
        else:
            st.error("Invalid email or password.")

if register_pressed:
    st.write("Redirecting to registration page...")
    st.switch_page("pages/register.py")

