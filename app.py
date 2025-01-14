import os
import streamlit as st
from importlib import import_module
from streamlit_navigation_bar import st_navbar

# 페이지별 모듈 매핑
pages = {
    "Home": "home",
    "뉴스 트렌드": "news_trend",
    "시장 지표": "data_table",
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
if page in pages:  # 선택된 페이지가 pages 딕셔너리에 있는지 확인
    current_page = pages[page]  # 딕셔너리에서 모듈 이름 가져오기
    module = import_module(current_page)  # 모듈 import
    module.render_page()  # render_page 함수 실행 (각 페이지 모듈에 정의)
