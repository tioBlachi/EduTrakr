# register.py

import streamlit as st
from database import create_user

def register_view():
    st.title("Register for EduTrakr")

    name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["Student", "Instructor"])

    if st.button("Create Account"):
        if name and email and password:
            success = create_user(email, password, role, name)
            if success:
                st.success("Account created! Please go back and log in.")
                st.session_state.page = "login"
                st.rerun()
            else:
                st.error("Email already exists.")
        else:
            st.warning("Please fill in all fields.")

    if st.button("Return to Login"):
        st.session_state.page = "login"
        st.rerun()
