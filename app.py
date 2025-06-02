"""
EduTrakr Main App

This is the main Streamlit app that launches the EduTrakr dashboard.
It sets the page configuration and displays the homepage UI elements.
see streamlit docs for more info
"""

import streamlit as st

st.set_page_config(page_title="EduTrakr", page_icon="📚")
st.title("📚 EduTrakr")
st.subheader("Your personal study time tracker")
st.write("Testing to see if live updates work, they do")

pressed = st.button("Press me")

if pressed:
    st.write("You pressed the button")
