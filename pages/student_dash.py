import streamlit as st
import utils as ut
import pandas as pd
import datetime  # may need later
import time

ss = st.session_state

name = ss.name
id = ss.user_id
role = ss.role

st.set_page_config(f"{name}'s Dashboard", page_icon='📚', layout='wide')
st.title(f'{name}\'s {role.capitalize()} Dashboard')

sessions = ut.get_study_sessions(id, "edutrakr.db")

df = pd.DataFrame(sessions, columns=["Session Id", "User ID", "Course Name", "Start Time", "End Time"])

st.divider()

df["Start Time"] = pd.to_datetime(df["Start Time"], format='ISO8601')
df["End Time"] = pd.to_datetime(df["End Time"], format='ISO8601')
df["Study Time"] = (df["End Time"] - df["Start Time"]).dt.total_seconds() / 60

st.dataframe(df)


#  Course Selection Dropdown 
course_names = df["Course Name"].unique().tolist()
#course_names = ut.get_courses(id, "edutrakr.db")

selected_course = st.selectbox("Select a Course", course_names)
displayed_course = df[df["Course Name"] == selected_course]
displayed_course["Date"] = displayed_course["Start Time"].dt.date

# ---- Line chart
summary = (
    displayed_course.groupby("Date")["Study Time"]
        .sum()
        .reset_index()
    )
st.markdown(f"### 📈 Study Time for {selected_course}")
st.line_chart(data=summary, x = "Date", y = "Study Time", use_container_width=True)

today = datetime.date.today()

st.subheader("Add a Study Session")
with st.form("add_study_session_form"):
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date")
        start_time = st.time_input("Start Time")
    with col2:
        end_date = st.date_input("End Date")#, min_value=start_date)
        end_time = st.time_input("End Time")
    
    submitted = st.form_submit_button("Add Session")
    if submitted:
        # could later convert from 24-hour format to 12-hour format
        start_datetime = datetime.datetime.combine(start_date, start_time)
        end_datetime = datetime.datetime.combine(end_date, end_time)

        if end_datetime <= start_datetime:
            st.warning("End time must be after start time")
        else: 
            # define insert_study_session in util.py
            ut.insert_study_session(id, selected_course, start_datetime, end_datetime, "edutrakr.db")
            st.success(f"Study session for '{selected_course}' has been added!")
            st.rerun()

st.subheader("Add a New Course")
with st.form("add_new_course_form"):
    new_course = st.text_input("Enter a new course name:")
    course_submit = st.form_submit_button("Add New Course")
    
    if course_submit:
        if not new_course.strip():
            st.warning("Please enter a valid course name")
        elif new_course.strip() in course_names:
            st.warning("Course already exists")
        else:
            # need to add course to the database
            try: 
                ut.insert_course(id, new_course.strip(), "edutrakr.db")
                st.success(f"Course '{new_course}' has been added to courses")
                st.rerun()
            except Exception as e:
                st.error(f"Failed to add course: {e}")

logout = st.button("Logout")

if logout:
    ss.clear()
    st.switch_page('login.py')
