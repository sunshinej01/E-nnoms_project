import streamlit as st
import subprocess

# 버튼으로 다른 Python 파일 실행
if st.button("다른 Python 파일 실행"):
    result = subprocess.run(["python", "other.py"], capture_output=True, text=True)
    st.write("### 실행결과")
    st.write(result.stdout) # 실행 결과 출력
    if result.stderr:
        st.write("### 에러")
        st.write(result.stderr)