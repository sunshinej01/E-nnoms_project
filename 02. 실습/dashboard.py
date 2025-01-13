import streamlit as st
import pandas as pd
import time

# 앱 제목
st.title("My Interactive Dashboard")

# 세션 상태 초기화
for key, value in {
    "data": [],
    "message": None,
    "message_time": None,
    "current_name": "",
    "current_age": 0,
    "current_score": 0.0,
}.items():
    if key not in st.session_state:
        st.session_state[key] = value

# 데이터 추가 함수
def add_data():
    if (st.session_state.current_name and
    st.session_state.current_age > 0 and
    st.session_state.current_score > 0):
        new_entry = {
            "Name": st.session_state.current_name,
            "Age": st.session_state.current_age,
            "Score": st.session_state.current_score,
        }
        st.session_state.data.append(new_entry)
        st.session_state.message = f"Data Added: {new_entry}"
    else:
        st.session_state.message = "Please fill all fields correctly!"
    st.session_state.message_time = time.time()
    st.session_state.current_name, st.session_state.current_age, st.session_state.current_score = "", 0, 0.0

# 메시지 초기화 함수
def clear_message():
    if (st.session_state.message and
        time.time() - st.session_state.message_time > 3):
        st.session_state.message, st.session_state.message_time = None, None

# 탭 생성
tabs = st.tabs(["User Inputs",
                "Data Display",
                "Data Analysis"])

# 1. User Inputs 탭
with tabs[0]:
    st.header("User Inputs")
    st.text_input("Enter Name", key="current_name")
    st.number_input("Enter Age", min_value=0, max_value=120, step=1, key="current_age")
    st.number_input("Enter Score", min_value=0.0, max_value=100.0, step=0.1, key="current_score")
    st.button("Add Data", on_click=add_data)
    if st.session_state.message:
        st.success(st.session_state.message)
        clear_message()

# 2. Data Display 탭
with tabs[1]:
    st.header("Data Display")
    if st.session_state.data:
        st.table(pd.DataFrame(st.session_state.data))
    else:
        st.write("No data available. Please add data in the 'User Inputs' tab.")

# 3. Data Analysis 탭
with tabs[2]:
    st.header("Data Analysis")
    if st.session_state.data:
        df = pd.DataFrame(st.session_state.data)
        
        # 나이와 점수 구간화
        bins_age = list(range(0, 130, 10))  # 나이 구간: 0-9, 10-19, ...
        bins_score = list(range(0, 110, 10))  # 점수 구간: 0-9, 10-19, ...
        df["Age Group"] = pd.cut(df["Age"], bins=bins_age, right=False, labels=[f"{i}-{i+9}" for i in bins_age[:-1]])
        df["Score Group"] = pd.cut(df["Score"], bins=bins_score, right=False, labels=[f"{i}-{i+9}" for i in bins_score[:-1]])
        
        # 사용자 선택: Age 또는 Score
        option = st.selectbox("Select Data to Analyze", ["Age", "Score"])
        if option == "Age":
            # 나이대별 카운트
            age_counts = df["Age Group"].value_counts(sort=False)
            st.subheader("Age Group Counts")
            st.bar_chart(age_counts)
        elif option == "Score":
            # 점수 구간별 카운트
            score_counts = df["Score Group"].value_counts(sort=False)
            st.subheader("Score Group Counts")
            st.bar_chart(score_counts)
    else:
        st.write("No data available. Please add data in the 'User Inputs' tab.")