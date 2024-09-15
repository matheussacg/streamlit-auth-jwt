import streamlit as st
from auth.state import get_state
from auth.menu import render_menu
from utils.styles import remove_st_decoration


remove_st_decoration()

render_menu()

state = get_state()

if not state.authenticated:
    st.warning("Please log in to access this page.")
    st.switch_page("app.py")

if state.role not in ["admin", "super-admin"]:
    st.warning("You do not have permission to view this page.")
    st.stop()

st.title("This page is available to all admins")
st.markdown(f"You are currently logged with the role of {state.role}.")