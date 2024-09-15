import streamlit as st
from dotenv import load_dotenv
import os
import requests
from extra_streamlit_components import CookieManager
import jwt

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()
API_URL = os.getenv("API")
SECRET_KEY = os.getenv("SECRET_KEY")

# Inicializa o Cookie Manager
cookie_manager = CookieManager()

def set_cookies(token):
    cookie_manager.set("access_token", token)

def get_cookies():
    return {
        "access_token": cookie_manager.get("access_token")
    }

def delete_cookies():
    cookie_manager.delete("access_token")

def decode_jwt(token):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded_token
    except jwt.ExpiredSignatureError:
        st.error("Token expirado. Faça login novamente.")
        delete_cookies()
        st.session_state.clear()
        return None
    except jwt.InvalidTokenError:
        st.error("Token inválido.")
        delete_cookies()
        st.session_state.clear()
        return None

def _check_password():
    """Authenticate user and manage login state."""
    # Verifica se já há cookies de autenticação
    cookies = get_cookies()

    if cookies["access_token"]:
        decoded_token = decode_jwt(cookies["access_token"])
        if decoded_token:
            st.session_state.authenticated = True
            st.session_state.username = decoded_token.get("sub")
            st.session_state.role = decoded_token.get("role")
            st.session_state.name = decoded_token.get("name")
            st.session_state.access_token = cookies["access_token"]
            return True

    if st.session_state.get("authenticated"):
        return True

    with st.form("Credentials"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Log in")

    if submitted:
        # Verifica as credenciais do usuário na API
        response = requests.post(f"{API_URL}/login/", json={"username": username, "password": password})

        if response.status_code == 200:
            # Se a autenticação for bem-sucedida, definir o estado da sessão e armazenar nos cookies
            result = response.json()
            st.session_state.access_token = result.get("access_token")
            
            # Decodificar o JWT para obter as informações do usuário
            decoded_token = decode_jwt(st.session_state.access_token)
            if decoded_token:
                st.session_state.authenticated = True
                st.session_state.username = decoded_token.get("sub")
                st.session_state.role = decoded_token.get("role")
                st.session_state.name = decoded_token.get("name")
                
                # Armazena o token nos cookies
                set_cookies(st.session_state.access_token)
                st.rerun()
        else:
            st.error("User not known or password incorrect.")

    return False

def _authenticated_menu():
    # Exibe um menu de navegação para usuários autenticados
    st.sidebar.page_link("app.py", label="Home Page", icon="🏡")
    st.sidebar.page_link("pages/user.py", label="Regular User Page", icon="🚎")
    if st.session_state.role in ["admin", "super-admin"]:
        st.sidebar.page_link("pages/admin.py", label="Admin User Page", icon="🌲")
        st.sidebar.page_link(
            "pages/super-admin.py",
            label="Super Admin User Page",
            icon="🌴",
            disabled=st.session_state.role != "super-admin",
        )
    st.sidebar.divider()
    st.sidebar.write(f"Bem vindo, {st.session_state.name}!")
    st.sidebar.write(f"Sua permissão é: {st.session_state.role}")
    if st.sidebar.button("Logout"):
        _logout()

def _unauthenticated_menu():
    pass

def _logout():
    """Log out the current user."""
    st.session_state.clear()
    delete_cookies()
    st.success("You have been logged out successfully.")
    st.rerun()

def menu():
    # Determina se um usuário está logado ou não e mostra o menu correto
    if not _check_password():
        _unauthenticated_menu()
        st.stop()
    else:
        _authenticated_menu()

def menu_with_redirect():
    # Redireciona usuários para a página principal se não estiverem logados
    if not _check_password():
        st.switch_page("app.py")
    menu()
