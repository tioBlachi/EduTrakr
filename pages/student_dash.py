import streamlit as st
import utils as ut
import pandas as pd
import datetime  # may need later

ss = st.session_state

name = ss.name
id = ss.user_id
role = ss.role

st.set_page_config(f"{name}'s Dashboard", page_icon='📚', layout='wide')
st.title(f'{name}\'s {role.capitalize()} Dashboard')

sessions = ut.get_study_sessions(id, "edutrakr.db")

df = pd.DataFrame(sessions, columns=["Session Id", "User ID", "Course Name", "Start Time", "End Time"])

st.divider()

df["Start Time"] = pd.to_datetime(df["Start Time"])
df["End Time"] = pd.to_datetime(df["End Time"])
df["Study Time"] = (df["End Time"] - df["Start Time"]).dt.total_seconds() / 60

st.dataframe(df)

# (Blas) I was able to add a Study Time column to the dataframe created with get_study_sessions
# These are tasks that I think need to get done for this dashboard
# If I am missing anything please just let me know 
# Don't worry about how everything looks for now
# The main thing is that everything is functional 
# Aesthetics and the instructor dashboard will be the focus of Sprint 2

# TODO: Student Dashboard Development Tasks

# --- Alex's Tasks ---
# 1. Course Selection Dropdown
#    - Get unique course names from the DataFrame of study sessions.
#    - Use st.selectbox to let the user choose a course.
#    - Store the selection in a variable like `selected_course`.
#    - Filter the DataFrame based on that selection (e.g., displayed_course = df[df["Course Name"] == selected_course]).

# 2. Display Refresh
#    - Ensure that after adding a course or a study session, the Streamlit widgets update accordingly.
#    - Use session state or conditional logic to handle rerendering components as needed.

# --- Adam's Tasks ---
# 1. Line Chart of Study Time
#    - Add a new "Date" column using `.dt.date` from the filtered course’s Start Time.
#    - Group the filtered DataFrame by "Date" and calculate the total "Study Time" per day.
#    - Use st.line_chart to display the daily study time for the selected course.

# 2. Optional Enhancements
#    - Calculate and display total study time for the currently selected course (sum the "Study Time" column).
#    - Check that the end time is always after the start time when adding sessions and show a warning if not.

# --- Jacob's Tasks ---
# 1. Add Study Session UI
#    - Create inputs to select start and end date/time (`st.date_input`, `st.time_input`).
#    - Combine those into start_datetime and end_datetime using `datetime.combine()`.
#    - Add a button or form to submit the data.
#    - When submitted, call a function to insert the session into the database (needs to include user_id and selected_course).
#    - Update the main DataFrame with the new session so the chart reflects the addition.

# 2. Add New Course Option
#    - Use a `st.text_input` to let the user type a new course name.
#    - When submitted, insert it into the user’s course list in the database.
#    - Ensure the dropdown options are refreshed to include the new course.

# --- Stretch Goal for Anyone ---
# - Check for duplicate course names before inserting into the database.
# - Consider sorting the dropdown list alphabetically or by most recent.

logout = st.button("Logout")

if logout:
    ss.clear
    st.switch_page('login.py')