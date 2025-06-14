import streamlit as st

def instructor_dashboard():
    name = st.session_state.get("name", "Instructor")
    st.title(f"Professor {name}'s Dashboard")