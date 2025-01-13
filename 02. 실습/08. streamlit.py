import streamlit as st
import pandas as pd
# ------------- 1. streamlit 설치 ----------------------
# 앱 제목 설정
st.title('첫 번째 Streamlit 앱')
# 텍스트 출력
st.write('안녕하세요! Streamlit입니다.')
st.write('오늘은 스트림릿을 배울거에요.')
# 이미지 출력
st.image('streamlit_logo.png', width=200)
# 데이터 프레임 생성
data = {'name': ['Alice', 'Bob', 'Charlie'], 'age': [30, 25, 22]}
df = pd.DataFrame(data)
# 데이터 프레임 출력
st.dataframe(df)
# 막대 그래프 생성
st.bar_chart(df['age'])

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
# 한글 폰트 설정 (전역)
plt.rcParams['font.family'] = 'AppleGothic'
# 마이너스 폰트 깨짐 방지
plt.rcParams['axes.unicode_minus'] = False
# 앱 제목 설정
st.title("첫 번째 Streamlit 앱")
# 데이터프레임 생성
data = {'name': ['Alice', 'Bob', 'Charlie', 'Emma'],
        'age': [30, 25, 22, 21],
        'gender': ['Female', 'Male', 'Male', 'Female']}
df = pd.DataFrame(data)
# 데이터 프레임 출력
st.dataframe(df)
# 데이터 프레임 정렬
sorted_df = df.sort_values(by="age")
# 데이터 프레임 집계
average_age = sorted_df["age"].mean()
st.write("")
# 정렬된 데이터 프레임 출력
st.write('정렬된 데이터 프레임')
st.dataframe(sorted_df)
# 평균 연령 출력
# unsafe_allow_html=True HTML을 작성할 수 있게 함
st.write("평균 연령:", round(average_age, 4))
st.markdown(
    f"""
    <h1 style='font-size:32px; color:white;'>
        평균 연령: <span style='color:yellow;'>{round(average_age, 4)}</span>
    </h1>
    """,
    unsafe_allow_html=True
)
# 성별별 연령 분포 그래프
plt.figure(figsize=(8, 6))
sns.barplot(data=df, x="gender", y="age", ci=None, palette="Set2")
plt.xlabel("성별")
plt.ylabel("나이")
plt.title("성별별 평균 연령 분포")
st.pyplot(plt)

# page_title 페이지 제목 설정
st.set_page_config(page_title="홈페이지",
                   page_icon=":sunglasses:")

# 이후 Streamlit 명령어 사용
st.title('라디오 버튼 페이지')

import streamlit as st
import uuid
# 세션 ID 생성 및 유지
if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())  # 고유 세션 ID 생성
# 세션 ID 출력
st.write("### 세션 ID")
st.write(f"Session ID: {st.session_state['session_id']}")
# 일반 변수와 세션 상태 변수 비교
if "normal_counter" not in st.session_state:
    normal_counter = 0  # 일반 변수 초기화
if "session_counter" not in st.session_state:
    st.session_state["session_counter"] = 0  # 세션 상태 변수 초기화
increment_normal = st.button("일반 변수 증가")
increment_session = st.button("세션 상태 증가")
if increment_normal:
    normal_counter += 1
if increment_session:
    st.session_state["session_counter"] += 1
# 출력
st.write("### 일반 변수 카운터 (normal_counter)")
st.write(f"Normal Counter: {locals().get('normal_counter', 0)}")
st.write("### 세션 상태 카운터 (st.session_state)")
st.write(f"Session State Counter: {st.session_state['session_counter']}")
st.write("### 일반 변수와 세션 상태 차이점")
st.write("""
1. **일반 변수**: 앱이 매번 재실행될 때마다 초기화됩니다. 버튼 클릭 후에도 값이 저장되지 않고 사라집니다.
2. **세션 상태 (`st.session_state`)**: 앱이 재실행되어도 같은 세션 내에서 값을 유지합니다. 버튼을 클릭하면 이전 값이 유지되며 계속 증가합니다.
""")
st.write(st.session_state)