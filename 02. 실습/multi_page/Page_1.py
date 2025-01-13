import streamlit as st

def render_page(change_page):
    st.title("페이지 1")
    st.write("여기서는 특정 작업을 합니다. 조건이 충족되면 페이지 2로 이동합니다.")
    user_input = st.text_input("10을 입력하면 페이지 2로 이동합니다:", "")
    if user_input == "10":
        change_page("Page2")
    if st.button("홈으로 돌아가기"):
        change_page("Home")
