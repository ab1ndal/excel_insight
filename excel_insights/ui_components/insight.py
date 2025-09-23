import streamlit as st

def specify_insight():
    return st.session_state.get("insight_spec", None)