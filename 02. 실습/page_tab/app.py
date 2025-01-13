import streamlit as st
from tabs import inputs_tab, display_tab, analysis_tab
from state import initialize_state

# 앱 초기화
initialize_state()

# 앱 제목
st.title("My Interactive Dashboard")

# 탭 생성
tabs = st.tabs(["User Inputs", "Data Display", "Data Analysis"])

# 각 탭 실행
with tabs[0]:
    inputs_tab.render()

with tabs[1]:
    display_tab.render()

with tabs[2]:
    analysis_tab.render()
