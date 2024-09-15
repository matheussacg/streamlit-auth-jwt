import streamlit as st
from app import remove_menu_items
from auth.menu import menu_with_redirect

remove_menu_items()

# Redirect to app.py if not logged in, otherwise show the navigation menu
menu_with_redirect()

st.title("This page is available to all users")
st.markdown(f"You are currently logged with the role of {st.session_state.role}.")