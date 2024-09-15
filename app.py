import streamlit as st
st.set_page_config(page_title="Home Page", page_icon="🏡")
from auth.menu import menu


def remove_menu_items():
	st.markdown("""
	<style>
		[data-testid="stDecoration"] {
			display: none;
		}

	</style>""",
	unsafe_allow_html=True)
 
remove_menu_items()
menu()

# Here goes your normal streamlit app
st.title("This page is available to all users")
st.markdown(f"You are currently logged with the role of {st.session_state.role}.")
