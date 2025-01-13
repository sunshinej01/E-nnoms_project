import streamlit as st

def render_page(change_page):
    st.title("홈 페이지")
    st.write("이곳은 홈입니다. 페이지 1로 이동하려면 버튼을 클릭하세요.")
    if st.button("페이지 1로 이동"):
        change_page("Page1")
