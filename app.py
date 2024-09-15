import streamlit as st
st.set_page_config(page_title="Home Page", page_icon="🏡")
from auth.state import get_state
from auth.menu import render_menu
from utils.styles import remove_st_decoration

remove_st_decoration()

render_menu()

state = get_state()
if state.authenticated:
    st.title("This page is available to all users")
    st.markdown(f"You are currently logged with the role of {state.role}.")
else:
    st.title("Welcome")
    st.markdown("Please log in to access the application.")
