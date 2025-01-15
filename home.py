import streamlit as st
from streamlit_autorefresh import st_autorefresh
from datetime import datetime
import base64

def get_base64_image(image_path):
    with open(image_path, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()
    return encoded

def render_page():
    # 제목
    st.markdown(
    """
    <style>
    .fullscreen-title {
        font-size: 90px; /* 글씨 크기를 조정 */
        font-weight: bold; /* 굵게 */
        text-align: center; /* 중앙 정렬 */
        color: #333; /* 글씨 색상 */
        margin-top: -15px; /* 위쪽 여백 */
        margin-bottom: px; /* 아래쪽 여백 */
    }
    </style>

    <div class="fullscreen-title">
        &#128630; 
        E-nnoms 
        &#128631;
        <p><b2><h4 style= "font-weight: 900; color: black; margin-top: -25px; margin-bottom: 1px;"><em>Empowering Innovators</b2></p>
    </div>
    """,
    unsafe_allow_html=True,
    )
    
    # 이미지 경로
    image_path = "god2.jpg"
    base64_image = get_base64_image(image_path)

    # CSS와 HTML로 이미지 렌더링
    st.markdown(
        f"""
        <style>
        .responsive-img {{
            max-width: 100%;
            height: auto;
            display: block;
            margin: 0 auto;
        }}
        </style>
        <div>
            <img src="data:image/jpeg;base64,{base64_image}" alt="우리" class="responsive-img">
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # 시계
    st_autorefresh(interval=1000, limit=None)  # 1000ms = 1초마다 리프레시
    clock_placeholder = st.empty() 
    
    # 현재 시간 가져오기
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.markdown(
        f"""
        <div style="
            text-align: center; 
            font-size: 2rem; 
            font-weight: bold; 
            margin-top: 20px;
        ">
            {current_time}
        </div>
        """,
        unsafe_allow_html=True,
    )
 
    # 본문 가운데 정렬 및 들여쓰기
    st.markdown(
        """
        <hr style="border: 1px solid #ddd; margin: 20px 0;">
        <div class="centered-text", style="text-align: left;">
            <p><b2><h2 style= "font-weight: 900; margin-bottom: 10px;"> Project Name</b2></p>
            <p>네이버 뉴스와 시장지표를 활용한 대시보드 제작 프로젝트</p>
            <br>
            <br>
            <p><h2 style= "font-weight: 900; color: bblack; margin-bottom: 10px;">Intro</p>
            <p> 이 프로젝트는 네이버 뉴스 데이터를 수집하고, 주요 시장 지표와 결합하여<br> 직관적인 대시보드를 제공하는 것을 목표로 합니다.</p>
            <br>
            <br>
            <br>
            <br>
        </div>

        <div class="source", style="text-align: right;">
            <p><strong><h3>Team</strong></p>
            <p>장새영<br> 양새람<br> 조민희<br>채서린</p>
            <hr style="border: 1px solid #ddd; color: black; margin: 5px 0 2px 0;">
            <p style="margin-top: 0px;"><h6>Source</p>
            <p><h7>https://news.naver.com<br>https://finance.naver.com</p>
        """,
        unsafe_allow_html=True,
    )
