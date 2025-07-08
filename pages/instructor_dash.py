import streamlit as st

ss = st.session_state

name = ss.name
id = ss.user_id
role = ss.role

st.write(name)
st.write(id)
st.write(role)