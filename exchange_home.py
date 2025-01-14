import requests
import pandas as pd
from bs4 import BeautifulSoup

def merge_dataframes(*dataframes):
    # 모든 DataFrame을 병합하여 하나의 DataFrame으로 반환
    return pd.concat(dataframes, axis=1)

def collect_exchange_rates(tab, pg_num, name):
    rates = {}
    for pg in range(pg_num):  # 기본 페이지에서는 30일치 데이터를 크롤링
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

# 사용 예시
pg_num = 3
names = [
    '미국 USD', '유럽연합 EUR', '일본 JPY (100엔)'
]
currency_list = [
    "USD", "EUR", "JPY"
]

# 각 통화에 대해 collect_exchange_rates를 호출하고 결과를 merge_dataframes로 합치기
dataframes = []
for tab, name in zip(currency_list, names):
    df = collect_exchange_rates(tab, pg_num, name)
    dataframes.append(df)

# merge_dataframes로 최종 DataFrame 생성
final_exchange_df = merge_dataframes(*dataframes)

# 결과 출력
print(final_exchange_df)
