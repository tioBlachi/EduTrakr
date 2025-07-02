"""
EduTrakr Main App

This is the main Streamlit app that launches the EduTrakr dashboard.
It sets the page configuration and displays the homepage UI elements.
see streamlit docs for more info
"""

import streamlit as st

# Page configuration
st.set_page_config(page_title="EduTrakr", page_icon="📚")
st.title("📚 EduTrakr")
st.subheader("Your personal study time tracker")

# Input fields
username = st.text_input("Username")
password = st.text_input("Password", type="password")

# Login button
login_pressed = st.button("Login")

# Register button (below login)
register_pressed = st.button("Register")

# Actions
if login_pressed:
    st.write(f"Attempting to log in user: `{username}`")
    # authenticate_user(username, password)

if register_pressed:
    st.write("Redirecting to registration page...")
    st.switch_page("pages/register.py")

