import streamlit as st
from auth.state import get_state
from auth.menu import render_menu

def remove_menu_items():
    st.markdown("""
    <style>
        [data-testid="stDecoration"] {
            display: none;
        }
    </style>""", unsafe_allow_html=True)

remove_menu_items()
render_menu()

state = get_state()

if not state.authenticated:
    st.warning("Please log in to access this page.")
    st.switch_page("app.py")

if state.role != "super-admin":
    st.warning("You do not have permission to view this page.")
    st.stop()

st.title("This page is available to super-admins")
st.markdown(f"You are currently logged with the role of {state.role}.")