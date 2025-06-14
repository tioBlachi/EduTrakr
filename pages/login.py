"""
Authentication Module (To be implemented)

This file will handle user authentication using streamlit-authenticator.
Currently empty, but reserved for login and user management logic.
"""

import streamlit as st
from database import authenticate_user, get_user_name  # import new helper

def login_view():
    st.title("Welcome to EduTrakr!")
    st.subheader("Login to Your Account")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        role = authenticate_user(email, password)
        if role:
            name = get_user_name(email, role)
            if not name:
                st.error("Name not found in database.")
                return

            st.success(f"Logged in as {role.capitalize()}")

            # Store in session state
            st.session_state.authenticated = True
            st.session_state.email = email
            st.session_state.role = role
            st.session_state.name = name

            # Route to correct dashboard
            if role == "student":
                st.session_state.page = "student_dash"
            else:
                st.session_state.page = "instructor_dash"

            st.rerun()
        else:
            st.error("Invalid email or password")

    st.write("Don't have an account?")
    if st.button("Register"):
        st.session_state.page = 'register'
        st.rerun()

