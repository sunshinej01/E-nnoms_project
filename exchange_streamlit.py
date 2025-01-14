import pandas as pd
import plotly.graph_objs as go
import exchange_home as ex

def get_exchange_data():
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

    return final_exchange_df, names

def create_exchange_figure(final_exchange_df, names):
    fig = go.Figure()

    for i, name in enumerate(names):
        line_color = 'fuchsia' if name == 'JPY' else None  # 'JPY'의 색상을 푸시아로 설정
        fig.add_trace(go.Scatter(x=final_exchange_df.index, y=final_exchange_df.iloc[:, i],
                                 mode='lines', name=name, line=dict(color=line_color)))

    # 그래프 레이아웃 설정
    fig.update_layout(title="환율 변화",
                      xaxis_title="날짜",
                      yaxis_title="환율",
                      yaxis=dict(range=[final_exchange_df.min().min() - 1, final_exchange_df.max().max() + 1]),
                      xaxis=dict(tickformat="%Y-%m-%d"))  # x축 날짜 형식 설정

    return fig

def prepare_data_table(final_exchange_df):
    # 데이터프레임 인덱스를 열로 변환
    final_exchange_df.reset_index(inplace=True)

    # 열 이름 변경 및 순서 조정
    names = ['USD', 'EUR', 'JPY']
    final_exchange_df.columns = ['날짜'] + names + ['USD 등락', 'EUR 등락', 'JPY 등락']  # 열 이름 변경
    final_exchange_df = final_exchange_df[['날짜', 'USD', 'USD 등락', 'EUR', 'EUR 등락', 'JPY', 'JPY 등락']]  # 열 순서 조정

    return final_exchange_df

def colorize_dataframe(df):
    html = df.copy()

    for col in ['USD 등락', 'EUR 등락', 'JPY 등락']:
        html[col] = html[col].apply(
            lambda x: "<span style='color: black;'>-</span>" if x == 0 else (f"<span style='color: red;'>{x:.2f}</span>" if x > 0 else f"<span style='color: blue;'>{x:.2f}</span>")
        )
    
    return html.to_html(escape=False, index=False, justify='center')
