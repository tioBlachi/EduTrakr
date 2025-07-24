import streamlit as st
import utils as ut
import pandas as pd

ss = st.session_state
name = ss.get("name", "Unknown")
id = ss.get("user_id", -1)
role = ss.get("role", "instructor")

st.set_page_config(f"{name}'s Instructor Dashboard", page_icon='🧑‍🏫', layout='wide')
st.title(f"{name}'s {role.capitalize()} Dashboard")
st.divider()



# UI to select course
instructor_id = st.session_state.get("user_id")
courses = ut.get_courses_for_instructor(instructor_id)
course_names = ["All Courses"] + [course["name"] for course in courses]
selected_course = st.selectbox("Select a course", course_names)

if selected_course == "All Courses":
    student_ids = ut.get_all_visible_students_for_instructor(instructor_id)
    #sessions = ut.get_study_sessions_for_students(student_ids)
    # Get course_ids that this instructor teaches
    course_ids = [course["id"] for course in courses]

    # Filter sessions to only these courses
    sessions = ut.get_study_sessions_for_students(student_ids, course_ids=course_ids)

else:
    course_id = next(c["id"] for c in courses if c["name"] == selected_course)
    student_ids = ut.get_visible_students_for_course(course_id)
    sessions = ut.get_study_sessions_for_students(student_ids, course_id=course_id)

df = ut.format_sessions_to_dataframe(sessions)
st.dataframe(df)




if not df.empty:
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download as CSV", data=csv, file_name="study_sessions.csv", mime='text/csv')    

st.subheader("Summary")

if "Student Name" in df.columns:
    st.markdown(f"**Total Students Shown:** {df['Student Name'].nunique()}")

if "Study Duration (min)" in df.columns:
    st.markdown(f"**Total Study Time (min):** {df['Study Duration (min)'].sum():.2f}")



if st.button("Logout"):
    ss.clear()
    st.switch_page("login.py")
