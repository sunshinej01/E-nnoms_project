import streamlit as st
import pandas as pd

def render_page():
    st.header("시장지표")
    st.write("1. 환전고시환율")

    # 환율 데이터 (임시 데이터)
    exchange_rates = {
        "날짜": ["09:00", "09:30", "10:00", "10:30", "11:00"],
        "달러": [1320.50, 1321.00, 1321.50, 1322.00, 1322.50],
        "전일대비(달러)": [0.50, 0.00, 0.50, 0.50, 0.50],
        "엔화": [950.32, 950.85, 951.38, 951.91, 952.44],
        "전일대비(엔화)": [-0.48, 0.53, 0.53, 0.53, 0.53],
        "유로": [1420.75, 1421.28, 1421.81, 1422.34, 1422.87],
        "전일대비(유로)": [0.53, 0.53, 0.53, 0.53, 0.53],
    }

    # DataFrame 생성
    df = pd.DataFrame(exchange_rates)

    # 전일대비 컬럼 소수점 둘째 자리까지 표시
    df['전일대비(달러)'] = df['전일대비(달러)'].apply(lambda x: f'{x:.2f}')
    df['전일대비(엔화)'] = df['전일대비(엔화)'].apply(lambda x: f'{x:.2f}')
    df['전일대비(유로)'] = df['전일대비(유로)'].apply(lambda x: f'{x:.2f}')

    # 스타일 적용
    st.markdown(
        """
        <style>
        .rising {
            color: red;
        }
        .falling {
            color: blue;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # 테이블 HTML 생성
    table_html = "<table><thead><tr>"
    for col in df.columns:
        table_html += f"<th>{col}</th>"
    table_html += "</tr></thead><tbody>"
    for i in range(len(df)):
        table_html += "<tr>"
        for col in df.columns:
            if "전일대비" in col:
                value = float(df[col][i])
                table_html += f"<td class='{'rising' if value >= 0 else 'falling'}'>{value}</td>"
            else:
                table_html += f"<td>{df[col][i]}</td>"
        table_html += "</tr>"
    table_html += "</tbody></table>"

    # 테이블 출력
    st.markdown(table_html, unsafe_allow_html=True)

