import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import exchange_home as ex

# Streamlit 애플리케이션 제목
st.title("시장지표-환율")

# 환율 추이 소제목
st.subheader("환율 추이")

# 통화 목록 및 이름 정의
names = ['미국 USD', '유럽연합 EUR', '일본 JPY (100엔)']
currency_list = ["USD", "EUR", "JPY"]

# 기본값으로 3개 데이터 로드
pg_num = 3

# 최종 환율 DataFrame 가져오기
final_exchange_df = ex.get_final_exchange_rates(currency_list, names, pg_num)

# 데이터프레임을 수치형으로 변환
final_exchange_df = final_exchange_df.apply(pd.to_numeric, errors='coerce')

# 데이터 순서 거꾸로 바꾸기
final_exchange_df = final_exchange_df[::-1]

# Plotly를 사용하여 그래프 그리기
fig = go.Figure()

# 기본 색상과 레드 범례를 그린으로 변경
for i, name in enumerate(names):
    color = 'fuchsia' if name == '일본 JPY (100엔)' else None  # 일본 JPY의 색상을 그린으로 설정
    fig.add_trace(go.Scatter(x=final_exchange_df.index, y=final_exchange_df.iloc[:, i],
                             mode='lines', name=name, line=dict(color=color)))

# x축 구간을 10단위로 설정
fig.update_layout(title="환율 변화",
                  xaxis_title="날짜",
                  yaxis_title="환율",
                  yaxis=dict(range=[final_exchange_df.min().min() - 1, final_exchange_df.max().max() + 1]),
                  xaxis_tickangle=-45)

# x축 간격 설정 및 마지막 x축 구간 범위 표시
tick_values = list(range(0, len(final_exchange_df), 10))  # 10단위로 x축 값 생성
tick_labels = [str(final_exchange_df.index[i]) for i in tick_values]  # x축 레이블 생성

# 마지막 데이터의 날짜 추가
last_index = len(final_exchange_df) - 1
if last_index not in tick_values:
    tick_values.append(last_index)
    tick_labels.append(str(final_exchange_df.index[last_index]))

# tick_values와 tick_labels 정렬
tick_values.sort()
tick_labels = [tick_labels[tick_values.index(i)] for i in tick_values]

fig.update_xaxes(tickvals=tick_values, ticktext=tick_labels)  # x축 값과 레이블 설정

# Streamlit에 그래프 표시
st.plotly_chart(fig)

# 환율 데이터 소제목
st.subheader("환율 데이터")

# 데이터프레임을 표로 표시
# 열 이름을 하이퍼링크로 변경
for i, name in enumerate(names):
    final_exchange_df.rename(columns={final_exchange_df.columns[i]: f'<a href="http://example.com/{currency_list[i]}">{name}</a>'}, inplace=True)

# HTML로 표 표시 (역순으로 출력)
st.markdown(final_exchange_df[::-1].to_html(escape=False, index=True), unsafe_allow_html=True)
