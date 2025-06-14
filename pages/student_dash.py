import streamlit as st

def student_dashboard():
    name = st.session_state.get("name", "Student")
    st.title(f"{name}'s Dashboard")