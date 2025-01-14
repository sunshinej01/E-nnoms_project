import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime, timedelta
from data_crawler import crawl_data

# URL 설정
urls = {
    "휘발유": "https://finance.naver.com/marketindex/oilDailyQuote.naver?marketindexCd=OIL_GSL",
    "고급 휘발유": "https://finance.naver.com/marketindex/oilDailyQuote.naver?marketindexCd=OIL_HGSL",
    "경유": "https://finance.naver.com/marketindex/oilDailyQuote.naver?marketindexCd=OIL_LO"
}

# 제목


# 스타일을 적용하여 버튼을 하나의 행으로 배치하고 오른쪽 정렬
st.markdown(
    """
    <style>
    .button-container {
        display: flex;
        justify-content: flex-end;
        align-items: center;
        margin-top: -10px; /* 간격 조정 */
    }
    .button-container button {
        margin-left: 10px; /* 버튼 간격 */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 버튼 배치
st.markdown("<div class='button-container'>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns([5, 1, 1, 1])  # 버튼의 비율
with col1:
    st.write("### 국내 유가 지표 변화 그래프")
with col2:
    btn_1w = st.button("1주일", key="1w")
with col3:
    btn_3m = st.button("3개월", key="3m")
with col4:
    btn_6m = st.button("6개월", key="6m")
st.markdown("</div>", unsafe_allow_html=True)

# 기준 날짜 계산
today = datetime.now()
if btn_1w:
    start_date = today - timedelta(weeks=1)
    selected_period = "1주일"
elif btn_3m:
    start_date = today - timedelta(days=90)
    selected_period = "3개월"
elif btn_6m:
    start_date = today - timedelta(days=180)
    selected_period = "6개월"
else:
    # 기본값: 1주일
    start_date = today - timedelta(weeks=1)
    selected_period = "1주일"


# 데이터 크롤링
all_data = {}
for label, url in urls.items():
    df = crawl_data(url, start_date)
    df = df.sort_values("날짜")
    all_data[label] = df

# 데이터 시각화
traces = []
for label, df in all_data.items():
    traces.append(go.Scatter(
        x=df["날짜"],
        y=df["종가"],
        mode="lines",
        name=label,
        hoverinfo="x+y",
        marker={"symbol": "circle", "size": 8}
    ))

fig = {
    "data": traces,
    "layout": go.Layout(
        xaxis={"title": "날짜"},
        yaxis={"title": "종가 (원)"},
        template="plotly_white",
        hovermode="x",  # 마우스가 있는 x축에서만 마커 표시
        legend=dict(orientation="h", yanchor="top", y=1.3, xanchor="right", x=1)  # 범례 크기 조정
    )
}

st.plotly_chart(fig)
