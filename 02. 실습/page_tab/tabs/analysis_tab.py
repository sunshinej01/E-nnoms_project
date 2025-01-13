import streamlit as st
import pandas as pd

def render():
    """Data Analysis 탭을 렌더링합니다."""
    st.header("Data Analysis")
    if st.session_state.data:
        df = pd.DataFrame(st.session_state.data)

        # 나이와 점수 구간화
        bins_age = list(range(0, 130, 10))
        bins_score = list(range(0, 110, 10))
        
        df["Age Group"] = pd.cut(df["Age"], bins=bins_age, right=False, labels=[f"{i}-{i+9}" for i in bins_age[:-1]])
        df["Score Group"] = pd.cut(df["Score"], bins=bins_score, right=False, labels=[f"{i}-{i+9}" for i in bins_score[:-1]])

        # 사용자 선택
        option = st.selectbox("Select Data to Analyze", ["Age", "Score"])

        if option == "Age":
            age_counts = df["Age Group"].value_counts(sort=False)
            st.subheader("Age Group Counts")
            st.bar_chart(age_counts)

        elif option == "Score":
            score_counts = df["Score Group"].value_counts(sort=False)
            st.subheader("Score Group Counts")
            st.bar_chart(score_counts)
    else:
        st.write("No data available. Please add data in the 'User Inputs' tab.")
