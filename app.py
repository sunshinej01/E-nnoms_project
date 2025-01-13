import streamlit as st
import pandas as pd

st.title('dashboard')

st.write('대시보드입니다!')

# 탭 생성
tab_titles = ['네이버 뉴스 크롤링 및 토픽 모델링', '수치형 데이터 시각화']
tabs = st.tabs(tab_titles)

# 데이터 전처리 탭에 콘텐츠 추가
with tabs[0]:
    st.header('1. 네이버 뉴스 크롤링 및 토픽 모델링')
    st.write('데이터 전처리를 수핼할 수 있는 곳입니다.')

with tabs[1]:
    st.header('2. 수치형 데이터 시각화')
    st.write('모델 훈련을 수핼할 수 있는 곳입니다.')