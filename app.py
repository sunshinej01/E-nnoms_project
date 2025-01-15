import os
import streamlit as st
from importlib import import_module
from streamlit_navigation_bar import st_navbar
# 페이지별 모듈 매핑
pages = {
    "Home": "home",
    "News trend": "news_trend",
    "Market Data": "data_table",
}

# 세션 상태 초기화
if "page" not in st.session_state:
    st.session_state.page = "Home"  # 초기 페이지 설정

# GNB 스타일 설정
styles = {
    "nav": {
        "background-color": "white",
    },
    "span": {  # GNB 텍스트 스타일
        "color": "black",  # 검정색으로 변경
        "font-weight": "bold",  # 굵게 표시 (선택 사항)
    },
    "active": {  # 활성화된 탭 스타일
        "text-decoration": "underline",  # 밑줄 추가
    },
}

# GNB 생성
page = st_navbar(list(pages.keys()), styles=styles)

# 선택된 페이지에 따라 내용 표시
if page == "Home":
    module = import_module(pages["Home"])
    #st.title("Home")
    #st.write("홈 페이지입니다.")
elif page == "News trend":
    # news.py의 run_streamlit() 호출
    st.title("Home")
    st.write("홈 페이지입니다.")

elif page == "Market Data":
    st.title("Market Data")
    st.write("마켓 데이터를 준비 중입니다.")
