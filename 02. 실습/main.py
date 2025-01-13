import streamlit as st
import uuid
# 세션 ID 생성 및 유지
# st.session_state : 새로고침 해도 저장되는 값
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
2. **세션 상태(`st.session_state`)**: 앱이 재실행되어도 같은 세션 내에서 값을 유지합니다. 버튼을 클릭하면 이전 값이 유지되며 계속 증가합니다.
""")
st.write(st.session_state)