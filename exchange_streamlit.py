import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import exchange_home as ex

# Streamlit 애플리케이션 제목
st.title("시장지표-환율")

# 환율 추이 소제목
st.subheader("환율 추이")

# 통화 목록 및 이름 정의
names = ['USD', 'EUR', 'JPY']
currency_list = ["USD", "EUR", "JPY"]

# 기본값으로 3개 데이터 로드
pg_num = 3

# 최종 환율 DataFrame 가져오기
final_exchange_df = ex.get_final_exchange_rates(currency_list, names, pg_num)

# 데이터프레임을 수치형으로 변환
final_exchange_df = final_exchange_df.apply(pd.to_numeric, errors='coerce')

# 변동률 열 추가
ex.add_rate_changes(final_exchange_df)

# 데이터 순서 거꾸로 바꾸기
final_exchange_df = final_exchange_df[::-1]

# 날짜를 인덱스로 설정
final_exchange_df.index = pd.to_datetime(final_exchange_df.index)

# Plotly를 사용하여 그래프 그리기
fig = go.Figure()

for i, name in enumerate(names):
    line_color = 'fuchsia' if name == 'JPY' else None  # 'JPY'의 색상을 푸시아로 설정
    fig.add_trace(go.Scatter(x=final_exchange_df.index, y=final_exchange_df.iloc[:, i],
                             mode='lines', name=name, line=dict(color=line_color)))

# 그래프 레이아웃 설정
fig.update_layout(title="환율 변화",
                  xaxis_title="날짜",  # x축 제목을 '날짜'로 변경
                  yaxis_title="환율",  # y축 제목을 '환율'로 변경
                  yaxis=dict(range=[final_exchange_df.min().min() - 1, final_exchange_df.max().max() + 1]),
                  xaxis=dict(tickformat="%Y-%m-%d"))  # x축 날짜 형식 설정

# x축 tick 설정
tick_values = list(range(0, len(final_exchange_df), max(1, len(final_exchange_df) // 10)))  # 10단위로 x축 값 생성
tick_labels = [final_exchange_df.index[i].strftime('%Y-%m-%d') for i in tick_values]  # x축 레이블 생성

# 마지막 데이터의 날짜 추가
last_index = len(final_exchange_df) - 1
if last_index not in tick_values:
    tick_values.append(last_index)
    tick_labels.append(final_exchange_df.index[last_index].strftime('%Y-%m-%d'))

# tick_values와 tick_labels 정렬
tick_values.sort()
tick_labels = [tick_labels[tick_values.index(i)] for i in tick_values]

# x축 값과 레이블 설정
fig.update_xaxes(tickvals=tick_values, ticktext=tick_labels, tickangle=45)  # 각도 조정 추가

# x축의 범위 및 눈금 설정
fig.update_xaxes(showgrid=True)  # 그리드 표시

# Streamlit에 그래프 표시
st.plotly_chart(fig)

# 환율 데이터 소제목
st.subheader("환율 데이터")

# 버튼을 한 줄에 나란히 배치
cols = st.columns(7)  # 버튼 배치용 열 생성

# 첫 번째 열에 타이틀 추가
with cols[0]:
    st.markdown("<h7 style='text-align: center;'><span style='font-weight: normal;'>통화를</span><br><span style='font-weight: normal;'>선택하세요</span></h7>", unsafe_allow_html=True)

for i, name in enumerate(names):
    with cols[2*i+1]:  # 각 열에 버튼 배치
        if st.button(name, key=name):  # 각 버튼에 고유한 키를 부여
            fig_selected = go.Figure()
            fig_selected.add_trace(go.Scatter(x=final_exchange_df.index,
                                               y=final_exchange_df[name],
                                               mode='lines',
                                               name=name))

            # 그래프 레이아웃 설정
            fig_selected.update_layout(title=f"{name} 환율 변화",
                                        xaxis_title="날짜",
                                        yaxis_title="환율",
                                        yaxis=dict(range=[final_exchange_df[name].min() - 1, final_exchange_df[name].max() + 1]),
                                        xaxis=dict(tickformat="%Y-%m-%d"))  # x축 날짜 형식 설정

            # x축 tick 설정
            tick_values_selected = list(range(0, len(final_exchange_df), max(1, len(final_exchange_df) // 10)))  # 10단위로 x축 값 생성
            tick_labels_selected = [final_exchange_df.index[i].strftime('%Y-%m-%d') for i in tick_values_selected]  # x축 레이블 생성

            # 마지막 데이터의 날짜 추가
            last_index_selected = len(final_exchange_df) - 1
            if last_index_selected not in tick_values_selected:
                tick_values_selected.append(last_index_selected)
                tick_labels_selected.append(final_exchange_df.index[last_index_selected].strftime('%Y-%m-%d'))

            # tick_values와 tick_labels 정렬
            tick_values_selected.sort()
            tick_labels_selected = [tick_labels_selected[tick_values_selected.index(i)] for i in tick_values_selected]

            # x축 값과 레이블 설정
            fig_selected.update_xaxes(tickvals=tick_values_selected, ticktext=tick_labels_selected, tickangle=45)  # 각도 조정 추가

            # x축의 범위 및 눈금 설정
            fig_selected.update_xaxes(showgrid=True)  # 그리드 표시

            # 그래프 출력
            st.plotly_chart(fig_selected)

# 데이터프레임 인덱스를 열로 변환
final_exchange_df.reset_index(inplace=True)

# 열 이름 변경 및 순서 조정
final_exchange_df.columns = ['날짜'] + names + ['USD 등락', 'EUR 등락', 'JPY 등락']  # 열 이름 변경
final_exchange_df = final_exchange_df[['날짜', 'USD', 'USD 등락', 'EUR', 'EUR 등락', 'JPY', 'JPY 등락']]  # 열 순서 조정

# 색상 적용을 위한 HTML 테이블 생성
def colorize_dataframe(df):
    html = df.copy()

    for col in ['USD 등락', 'EUR 등락', 'JPY 등락']:
        html[col] = html[col].apply(
            lambda x: "<span style='color: black;'>-</span>" if x == 0 else (f"<span style='color: red;'>{x:.2f}</span>" if x > 0 else f"<span style='color: blue;'>{x:.2f}</span>")
        )
    
    return html.to_html(escape=False, index=False, justify='center')

# CSS 스타일 추가
css = """
<style>
    table {
        width: 100%;  /* 테이블 너비를 100%로 설정 */
        table-layout: fixed;  /* 고정 레이아웃 사용 */
    }
    th, td {
        padding: 10px;  /* 셀 패딩 조정 */
        text-align: center;  /* 모든 셀 중앙 정렬 */
        overflow: hidden;  /* 넘치는 텍스트 숨기기 */
        text-overflow: ellipsis;  /* 넘치는 텍스트에 생략 부호 추가 */
        white-space: nowrap;  /* 텍스트 줄 바꿈 방지 */
    }
    th {
        text-align: center;  /* 헤더 셀 중앙 정렬 */
    }
</style>
"""

# 색상 적용된 HTML 테이블 생성
colored_html_table = colorize_dataframe(final_exchange_df)

# CSS와 함께 데이터프레임을 HTML로 변환하여 표시
st.markdown(css, unsafe_allow_html=True)
st.markdown(colored_html_table, unsafe_allow_html=True)
