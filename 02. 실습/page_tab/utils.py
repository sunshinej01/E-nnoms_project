import streamlit as st
import time

def add_data():
    """사용자 입력 데이터를 추가합니다."""
    if (st.session_state.current_name and 
        st.session_state.current_age > 0 and 
        st.session_state.current_score > 0):
        
        new_entry = {
            "Name": st.session_state.current_name,
            "Age": st.session_state.current_age,
            "Score": st.session_state.current_score,
        }
        st.session_state.data.append(new_entry)
        st.session_state.message = f"Data Added: {new_entry}"
    else:
        st.session_state.message = "Please fill all fields correctly!"
    
    st.session_state.message_time = time.time()
    st.session_state.current_name, st.session_state.current_age, st.session_state.current_score = "", 0, 0.0

def clear_message():
    """메시지를 일정 시간 후에 초기화합니다."""
    if (st.session_state.message and 
        time.time() - st.session_state.message_time > 3):
        st.session_state.message, st.session_state.message_time = None, None
