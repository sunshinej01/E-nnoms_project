import requests
import pandas as pd
from bs4 import BeautifulSoup

def merge_dataframes(*dataframes):
    # 모든 DataFrame을 병합하여 하나의 DataFrame으로 반환
    return pd.concat(dataframes, axis=1)

def collect_exchange_rates(tab, pg_num, name):
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
    df = pd.DataFrame(list(rates.items()), columns=['date', name])
    df.set_index('date', inplace=True)
    
    return df  # DataFrame을 반환

def get_final_exchange_rates(currency_list, names, pg_num):
    dataframes = []
    for tab, name in zip(currency_list, names):
        df = collect_exchange_rates(tab, pg_num, name)
        dataframes.append(df)

    # merge_dataframes로 최종 DataFrame 생성
    final_exchange_df = merge_dataframes(*dataframes)
    return final_exchange_df[::-1]  # 최종 DataFrame 반환

def get_individual_rates(currency, pg_num):
    # currency_list에서 선택한 한 가지 항목에 대해 환율 데이터를 수집
    name = currency  # 통화 이름을 currency로 설정
    df = collect_exchange_rates(currency, pg_num, name)
    return df  # 개별 DataFrame 반환

def add_rate_changes(df):
    # 'USD'의 변동률을 계산하여 새로운 열 추가
    df['USD 등락'] = df['USD'].astype(float).diff().fillna(0)
    df['EUR 등락'] = df['EUR'].astype(float).diff().fillna(0)
    df['JPY 등락'] = df['JPY'].astype(float).diff().fillna(0)

    df[['USD 등락', 'EUR 등락', 'JPY 등락']] = df[['USD 등락', 'EUR 등락', 'JPY 등락']].fillna('-')


