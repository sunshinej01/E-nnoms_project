import streamlit as st
import requests
import json
import plotly.graph_objects as go
import pandas as pd


def render_page():
    # Streamlit 앱 제목
    st.title("📈 미국 주식 정보")
    st.write("S&P Top 10 종목에 대한 전일 대비 금일 등락률을 보여줍니다.")

    # API 호출
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://m.stock.naver.com/worldstock/index/.INX/total"
    }
    url = "https://api.stock.naver.com/index/.INX/enrollStocks?page=1&pageSize=10"
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)

    # 데이터 추출
    stock_name = [item['stockName'] for item in data['stocks']]
    stock_price = [float(item['fluctuationsRatio']) for item in data['stocks']]

    # DataFrame 생성
    df = pd.DataFrame({'stockName': stock_name, 'fluctuationsRatio': stock_price})

    # Plotly 막대 그래프 생성
    fig = go.Figure(
        data=[
            go.Bar(
                x=df['stockName'],
                y=df['fluctuationsRatio'],
                marker_color=['red' if val >= 0 else 'blue' for val in df['fluctuationsRatio']],
                text=[f"+{val:.2f}%" if val >= 0 else f"{val:.2f}%" for val in df['fluctuationsRatio']],
                textposition='outside',
                width=0.4,
                marker_line_width=0,
            )
        ]
    )

    # 레이아웃 설정
    fig.update_layout(
        title="S&P 500 Top 10",
        yaxis_title="등락률 (%)",
        xaxis_tickangle=-45,
        xaxis_tickfont=dict(size=14),
        yaxis_tickfont=dict(size=14),
        title_font=dict(size=20),
        template="plotly_white",
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis={'showgrid': False},
        yaxis={'showgrid': True, 'gridwidth': 0.5, 'gridcolor': 'lightgrey'},
        shapes=[
            dict(
                type='line',
                x0=-0.5,
                x1=len(df['stockName']) - 0.5,
                y0=0,
                y1=0,
                line=dict(color='black', width=2)
            )
        ]
    )

    # Streamlit에 그래프 출력
    st.plotly_chart(fig)  # fig.show() 대신 st.plotly_chart(fig) 사용

    # 새로고침 버튼 오른쪽 정렬
    st.markdown(
        """
        <style>
        div.stButton > button:first-child {
            display: block;  /* 가운데 정렬을 위해 블록 요소로 설정 */
            margin: 0 auto;  /* 가운데 정렬 */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # 새로고침 버튼
    if st.button("새로고침"):
        # JavaScript 코드 실행
        st.components.v1.html(
            """
            <script>
            window.location.reload();
            </script>
            """
        )