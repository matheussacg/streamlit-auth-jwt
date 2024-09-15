import streamlit as st
from auth.state import get_state

def render_menu():
    state = get_state()
    if not state.check_authentication():
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Log in")
            if submitted and state.login(username, password):
                st.rerun()
    else:
        st.sidebar.page_link("app.py", label="Home Page", icon="🏡")
        st.sidebar.page_link("pages/user.py", label="Regular User Page", icon="🚎")
        if state.role in ["admin", "super-admin"]:
            st.sidebar.page_link("pages/admin.py", label="Admin User Page", icon="🌲")
            st.sidebar.page_link(
                "pages/super-admin.py",
                label="Super Admin User Page",
                icon="🌴",
                disabled=state.role != "super-admin",
            )
        st.sidebar.divider()
        st.sidebar.write(f"Bem vindo, {state.name}!")
        st.sidebar.write(f"Sua permissão é: {state.role}")
        if st.sidebar.button("Logout"):
            state.logout()
            st.rerun()