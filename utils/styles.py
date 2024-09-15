import streamlit as st

def remove_st_decoration():
    st.markdown("""
    <style>
        [data-testid="stDecoration"] {
            display: none;
        }
    </style>""", unsafe_allow_html=True)