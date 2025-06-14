"""
EduTrakr Main App

This is the main Streamlit controller that launches the EduTrakr app.
It sets the page configuration and displays the homepage UI elements.
see streamlit docs for more info
"""

import streamlit as st
from pages.login import login_view
from pages.register import register_view
from pages.student_dash import student_dashboard
from pages.instructor_dash import instructor_dashboard

# Set default page
if 'page' not in st.session_state:
    st.session_state.page = 'login'

# Navigation logic
if st.session_state.page == 'login':
    login_view()
elif st.session_state.page == 'register':
    register_view()
elif st.session_state.page == 'student_dash':
    student_dashboard()
elif st.session_state.page == 'instructor_dash':
    instructor_dashboard()
