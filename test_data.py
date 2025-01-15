import pandas as pd
import plotly.graph_objs as go
import streamlit as st
import requests
import pandas as pd
from bs4 import BeautifulSoup

def merge_dataframes(*dataframes):
    # 모든 DataFrame을 병합하여 하나의 DataFrame으로 반환
    return pd.concat(dataframes, axis=1)
def collect_exchange_rates(tab, pg_num):
    rates = {}
    for pg in range(pg_num):  # 기본 페이지에서는 지정된 수만큼 데이터를 크롤링
        # url 설정
        url = f"https://finance.naver.com/marketindex/exchangeDailyQuote.naver?marketindexCd=FX_{tab}KRW&page={pg+1}"
        # response get
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # 날짜별 환율 크롤링
        date_rows = soup.select('tbody tr')
        for row in date_rows:
            date = row.select_one('td.date').text.strip()
            num = row.select_one('td.num').text.strip().replace(',', '')
            rates[date] = num
    # DataFrame 생성
    df = pd.DataFrame(list(rates.items()), columns=['date', tab])
    df.set_index('date', inplace=True)
    return df  # DataFrame을 반환
def get_final_exchange_rates(currency_list, pg_num):
    dataframes = []
    for tab in currency_list:
        df = collect_exchange_rates(tab, pg_num)
        dataframes.append(df)
    # merge_dataframes로 최종 DataFrame 생성
    final_exchange_df = merge_dataframes(*dataframes)
    return final_exchange_df[::-1]  # 최종 DataFrame 반환
def get_individual_rates(currency, pg_num):
    # currency_list에서 선택한 한 가지 항목에 대해 환율 데이터를 수집
    name = currency  # 통화 이름을 currency로 설정
    df = collect_exchange_rates(currency, pg_num)
    return df  # 개별 DataFrame 반환
def add_rate_changes(df):
    # 'USD'의 변동률을 계산하여 새로운 열 추가
    df['USD 등락'] = df['USD'].astype(float).diff().fillna(0)
    df['EUR 등락'] = df['EUR'].astype(float).diff().fillna(0)
    df['JPY 등락'] = df['JPY'].astype(float).diff().fillna(0)
    df[['USD 등락', 'EUR 등락', 'JPY 등락']] = df[['USD 등락', 'EUR 등락', 'JPY 등락']].fillna('-')

def render_page():
    # Streamlit 애플리케이션 제목
    st.title("시장지표-환율")
    # 환율 추이 소제목
    st.subheader("환율 추이")
    # 통화 목록 및 이름 정의
    currency_list = ["USD", "EUR", "JPY"]
    # 기본값으로 3개 데이터 로드
    pg_num = 3
    # 최종 환율 DataFrame 가져오기
    final_exchange_df = get_final_exchange_rates(currency_list, pg_num)
    # 데이터프레임을 수치형으로 변환
    final_exchange_df = final_exchange_df.apply(pd.to_numeric, errors='coerce')
    # 변동률 열 추가
    add_rate_changes(final_exchange_df)
    # 데이터 순서 거꾸로 바꾸기
    final_exchange_df = final_exchange_df[::-1]
    # 날짜를 인덱스로 설정
    final_exchange_df.index = pd.to_datetime(final_exchange_df.index)
    # 그래프 생성
    fig = create_exchange_figure(final_exchange_df, currency_list)
    # Streamlit에 그래프 표시
    if 'show_graph' not in st.session_state:
        st.session_state.show_graph = True  # 초기값 설정
    if st.session_state.show_graph:
        st.plotly_chart(fig)
    # 환율 데이터 소제목
    st.subheader("환율 데이터")
    # 버튼을 한 줄에 나란히 배치
    cols = st.columns(10)  # 버튼 배치용 열 생성
    # 첫 번째 열에 타이틀 추가
    #with cols[0]:
    #    st.markdown("<h7 style='text-align: center;'><span style='font-weight: normal;'>통화를</span><br><span style='font-weight: normal;'>선택하세요</span></h7>", unsafe_allow_html=True)
    # 버튼 클릭 카운트 초기화
    if 'button_count' not in st.session_state:
        st.session_state.button_count = {name: 0 for name in currency_list}  # 각 통화 버튼의 카운트 초기화
    for i, name in enumerate(currency_list):
        with cols[7+i]:  # 각 열에 버튼 배치
            if st.button(name, key=name):  # 각 버튼에 고유한 키를 부여
                # 카운트 초기화 및 증가
                st.session_state.selected_currency = name  # 선택한 통화 저장
                st.session_state.show_graph = True  # 그래프 표시
                #st.rerun()  # 세션 리셋
    # 데이터프레임 준비
    final_exchange_df = prepare_data_table(final_exchange_df)
    # 통화 선택에 따른 페이지 분기
    if 'selected_currency' in st.session_state:
        selected_currency = st.session_state.selected_currency
        st.subheader(f"{selected_currency} 환율 데이터")
        # 선택된 통화에 대한 꺾은선 그래프 표시
        fig_currency = go.Figure()
        fig_currency.add_trace(go.Scatter(x=final_exchange_df['날짜'], y=final_exchange_df[selected_currency],
                                            mode='lines', name=selected_currency))
        fig_currency.update_layout(title=f"{selected_currency} 환율 변화",
                                    xaxis_title="날짜",
                                    yaxis_title="환율",
                                    xaxis=dict(tickformat="%Y-%m-%d"),
                                    yaxis=dict(range=[final_exchange_df[selected_currency].min() - 1,
                                                      final_exchange_df[selected_currency].max() + 1]))
        # Streamlit에 그래프 표시 (페이지 너비에 맞게 설정)
        st.plotly_chart(fig_currency, use_container_width=True)
    # 색상 적용된 HTML 테이블 생성
    colored_html_table = colorize_dataframe(final_exchange_df)
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
    # CSS와 함께 데이터프레임을 HTML로 변환하여 표시
    st.markdown(css, unsafe_allow_html=True)
    st.markdown(colored_html_table, unsafe_allow_html=True)
def get_exchange_data():
    # 통화 목록 및 이름 정의
    currency_list = ["USD", "EUR", "JPY"]
    # 기본값으로 3개 데이터 로드
    pg_num = 3
    # 최종 환율 DataFrame 가져오기
    final_exchange_df = get_final_exchange_rates(currency_list, pg_num)
    # 데이터프레임을 수치형으로 변환
    final_exchange_df = final_exchange_df.apply(pd.to_numeric, errors='coerce')
    # 변동률 열 추가
    add_rate_changes(final_exchange_df)
    # 데이터 순서 거꾸로 바꾸기
    final_exchange_df = final_exchange_df[::-1]
    # 날짜를 인덱스로 설정
    final_exchange_df.index = pd.to_datetime(final_exchange_df.index)
    return final_exchange_df, currency_list
def create_exchange_figure(final_exchange_df, currency_list):
    fig = go.Figure()
    for i, name in enumerate(currency_list):
        line_color = 'fuchsia' if name == 'JPY' else None  # 'JPY'의 색상을 푸시아로 설정
        fig.add_trace(go.Scatter(x=final_exchange_df.index, y=final_exchange_df.iloc[:, i],
                                 mode='lines', name=name, line=dict(color=line_color)))
    # 그래프 레이아웃 설정
    fig.update_layout(title="환율 변화",
                      xaxis_title="날짜",
                      yaxis_title="환율",
                      yaxis=dict(range=[800,1800]),#[final_exchange_df.min().min() - 1, final_exchange_df.max().max() + 1]),
                      xaxis=dict(tickformat="%Y-%m-%d"))  # x축 날짜 형식 설정
    return fig
def prepare_data_table(final_exchange_df):
    # 데이터프레임 인덱스를 열로 변환
    final_exchange_df.reset_index(inplace=True)
    # 열 이름 변경 및 순서 조정
    currency_list = ['USD', 'EUR', 'JPY']
    final_exchange_df.columns = ['날짜'] + currency_list + ['USD 등락', 'EUR 등락', 'JPY 등락']  # 열 이름 변경
    final_exchange_df = final_exchange_df[['날짜', 'USD', 'USD 등락', 'EUR', 'EUR 등락', 'JPY', 'JPY 등락']]  # 열 순서 조정
    return final_exchange_df
def colorize_dataframe(df):
    html = df.copy()
    for col in ['USD 등락', 'EUR 등락', 'JPY 등락']:
        html[col] = html[col].apply(
            lambda x: "<span style='color: black;'>-</span>" if x == 0 else (f"<span style='color: red;'>{x:.2f}</span>" if x > 0 else f"<span style='color: blue;'>{x:.2f}</span>")
        )
    return html.to_html(escape=False, index=False, justify='center')
#render_page()