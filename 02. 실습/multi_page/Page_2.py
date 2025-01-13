import streamlit as st

def render_page(change_page):
    st.title("페이지 2")
    st.write("이곳은 페이지 2입니다. 조건이 충족되어 여기에 도달했습니다.")
    if st.button("홈으로 돌아가기"):
        change_page("Home")
