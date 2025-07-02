import streamlit as st
import utils as util
import time
import re

st.markdown("<h1 style='text-align: center;'>Register for EduTrakr</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Create an EduTrakr Account</h3>", unsafe_allow_html=True)


registrationFormValues = {
    "firstName" : None,
    "lastName" : None, 
    "email" : None,
    "password": None,
    "verify-password": None,
    "role": None
}

with st.form(key="registrationInfoForm"):
    registrationFormValues["firstName"] = st.text_input("Enter your first name: ")
    registrationFormValues["lastName"] = st.text_input("Enter your last name: ")
    registrationFormValues["email"] = st.text_input("Please enter your email: ")
    registrationFormValues["password"] = st.text_input("Create a password: ")
    registrationFormValues["verify-password"] = st.text_input("Match password: ")
    registrationFormValues["role"] = st.selectbox("Role", ["Student", "Instructor"], index = 0)

    registrationButton = st.form_submit_button(label="Register", icon="📖", use_container_width= True )


if registrationButton: 
    # check if all form values are 
    if not all(registrationFormValues.values()):
        st.error("Please fill in all of the fields")

    else:
        firstName = registrationFormValues["firstName"].strip()
        lastName = registrationFormValues["lastName"].strip()
        email = registrationFormValues["email"].strip()
        password = registrationFormValues["password"]
        verifyPassword = registrationFormValues["verify-password"]
        emailRegex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        

        valid = True

        if not firstName.isalpha() or not lastName.isalpha:
            st.error("Please enter a valid first and late name")
            valid = False
        
        # check for email validation probably have to use re
        if not re.match(emailRegex, email):
            st.error(f"Invalid email. Please enter a valid email.")
            valid = False


        if len(password) < 6: 
            st.error("Password must be at least 6 characters long.")
            valid = False
        
        if password != verifyPassword:
            st.error("Passwords do not match.")
            valid = False

        if valid: 
            name = f"{firstName.capitalize()} {lastName.capitalize()}"
            role = registrationFormValues["role"].lower()

            if util.add_user(name, email, password, role):
                st.success("Registered successfully! Redirecting you to login page...")
                time.sleep(2)
                st.switch_page("login.py")
            else:
                st.error("Registration failed. User already exists")
    