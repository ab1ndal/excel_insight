import streamlit as st

def specify_insight():
    return st.session_state.get("plans", None)