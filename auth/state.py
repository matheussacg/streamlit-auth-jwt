import streamlit as st
from dotenv import load_dotenv
import os
import requests
import jwt
from extra_streamlit_components import CookieManager

load_dotenv()
API_URL = os.getenv("API")
SECRET_KEY = os.getenv("SECRET_KEY")

cookie_manager = CookieManager()

class SessionState:
    def __init__(self):
        self.authenticated = False
        self.username = None
        self.role = None
        self.name = None
        self.access_token = None

    def login(self, username, password):
        response = requests.post(f"{API_URL}/login/", json={"username": username, "password": password})
        if response.status_code == 200:
            result = response.json()
            self.access_token = result.get("access_token")
            decoded_token = self.decode_jwt(self.access_token)
            if decoded_token:
                self.authenticated = True
                self.username = decoded_token.get("sub")
                self.role = decoded_token.get("role")
                self.name = decoded_token.get("name")
                cookie_manager.set("access_token", self.access_token)
                return True
        else:
            st.error("Credenciais inválidas. Tente novamente.")
        return False

    def logout(self):
        self.authenticated = False
        self.username = None
        self.role = None
        self.name = None
        self.access_token = None
        cookie_manager.delete("access_token")

    def check_authentication(self):
        if not self.authenticated:
            access_token = cookie_manager.get("access_token")
            if access_token:
                decoded_token = self.decode_jwt(access_token)
                if decoded_token:
                    self.authenticated = True
                    self.username = decoded_token.get("sub")
                    self.role = decoded_token.get("role")
                    self.name = decoded_token.get("name")
                    self.access_token = access_token
        return self.authenticated

    @staticmethod
    def decode_jwt(token):
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            st.error("Token expirado. Faça login novamente.")
            return None
        except jwt.InvalidTokenError:
            st.error("Token inválido.")
            return None

def get_state():
    if 'session_state' not in st.session_state:
        st.session_state.session_state = SessionState()
    return st.session_state.session_state