import streamlit as st
import pandas as pd

def render():
    """Data Display 탭을 렌더링합니다."""
    st.header("Data Display")
    if st.session_state.data:
        st.table(pd.DataFrame(st.session_state.data))
    else:
        st.write("No data available. Please add data in the 'User Inputs' tab.")
