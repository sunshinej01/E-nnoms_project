import streamlit as st

st.markdown(
"""
<style>
div.stButton > button {
background-color: white;
color: black;
border: 2px so;lid #CCCCCC;
border-radius: 5px;
padding: 10px 20px;
font-size: 16px;
transition: background-color 0.3s, color 0.3s;
}
div.stButton > button:hover {
background-color: red;
color: white;
}
div.stDownloadButton > button:first-child {
float: right; # 오른쪽 정렬
}
</style>
""",
unsafe_allow_html=True
)

def render_page():
    # 제목
    st.markdown(
    "<h1 style='text-align: center;'>🍭E-nnoms Project🍭</h1>",
    unsafe_allow_html=True,
    )
    
    st.write("프로젝트명 : 네이버 뉴스와 시장지표를 활용한 대시보드 제작 프로젝트")
    st.write("프로젝트 소개 : ")
    st.write("팀 소개 : 장세영, 양새람, 조민희, 채서린")
