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

# ============================
# ALEX'S SECTION
# ============================

# Task: Create a dropdown to show only courses this instructor teaches
# - You'll need to implement get_courses_for_instructor(user_id) in utils.py
# - Add an "All Courses" option at the top of the dropdown

# Example:
# courses = ut.get_courses_for_instructor(id)
# course_options = ["All Courses"] + courses
# selected_course = st.selectbox("Select a course", course_options)

# ============================
# ADAM'S SECTION
# ============================


# UI to select course
instructor_id = st.session_state.get("instructor_id")
courses = ut.get_courses_for_instructor(instructor_id)
course_names = ["All Courses"] + [course["name"] for course in courses]
selected_course = st.selectbox("Select a course", course_names)

if selected_course == "All Courses":
    student_ids = ut.get_all_visible_students_for_instructor(instructor_id)
    sessions = ut.get_study_sessions_for_students(student_ids)
else:
    course_id = next(c["id"] for c in courses if c["name"] == selected_course)
    student_ids = ut.get_visible_students_for_course(course_id)
    sessions = ut.get_study_sessions_for_students(student_ids, course_id=course_id)

df = ut.format_sessions_to_dataframe(sessions)
st.dataframe(df)


# Task: Based on the selected course, retrieve all student study sessions
# - Exclude students with private = 1
# - If "All Courses" is selected, show sessions from all courses the instructor teaches
# - Implement supporting functions in utils.py as needed:
#     get_visible_students_for_course(course_id)
#     get_all_visible_students_for_instructor(instructor_id)

# - Convert sessions to a DataFrame with columns like:
#   "Student Name", "Course Name", "Start Time", "End Time", "Study Duration (min)"

# Example placeholder:
# df = pd.DataFrame([
#     {"Student Name": "Alice", "Course Name": "Python", "Start Time": "...", "End Time": "...", "Study Duration (min)": 45}
# ])
# st.dataframe(df)

# ============================
# JACOB'S SECTION
# ============================

# Task: Add download button to export the current filtered DataFrame as CSV
# - Only show the download button if df is not empty
# - Use st.download_button with utf-8 encoded CSV

# Example:
# if not df.empty:
#     csv = df.to_csv(index=False).encode('utf-8')
#     st.download_button("Download as CSV", data=csv, file_name="study_sessions.csv", mime='text/csv')

# Additional Task: Add a summary section showing (this is just a maybe):
# - Total number of non-private students displayed
# - Total study time across all sessions in the table

# Example:
# st.markdown(f"**Total Students Shown:** {df['Student Name'].nunique()}")
# st.markdown(f"**Total Study Time (min):** {df['Study Duration (min)'].sum()}")


if st.button("Logout"):
    ss.clear()
    st.switch_page("login.py")
