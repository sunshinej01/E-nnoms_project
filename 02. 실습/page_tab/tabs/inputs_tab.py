import streamlit as st
from utils import add_data, clear_message

def render():
    """User Inputs 탭을 렌더링합니다."""
    st.header("User Inputs")
    st.text_input("Enter Name", key="current_name")
    st.number_input("Enter Age", min_value=0, max_value=120, step=1, key="current_age")
    st.number_input("Enter Score", min_value=0.0, max_value=100.0, step=0.1, key="current_score")
    st.button("Add Data", on_click=add_data)
    if st.session_state.message:
        st.success(st.session_state.message)
        clear_message()
