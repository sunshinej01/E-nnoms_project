import time
from bs4 import BeautifulSoup
import requests
import datetime

def scrape_articles(next_value):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100"
    }

    # URL 구성
    url = f"https://news.naver.com/section/template/SECTION_ARTICLE_LIST?sid=100&sid2=&cluid=&pageNo=1&date=&next={next_value}&_=1736665778225"

    # 요청 보내기
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"요청 실패: {response.status_code}")
        return []

    # JSON 데이터 파싱
    temp = response.json()
    html_content = temp['renderedComponent']['SECTION_ARTICLE_LIST']

    # BeautifulSoup으로 파싱
    soup = BeautifulSoup(html_content, 'html.parser')
    articles = soup.find_all('li', class_='sa_item')

    # 기사 데이터 저장
    article_list = []
    for article in articles:
        title_tag = article.find('a', class_='sa_text_title')
        datetime_tag = article.find(class_='sa_text_datetime')  # 날짜 정보가 있는 태그

        if title_tag and datetime_tag:
            title = title_tag.get_text(strip=True)
            link = title_tag.get('href')
            date_str = datetime_tag.get_text(strip=True)  # 날짜 추출

            article_list.append((title, link, date_str))  # 제목, 링크, 날짜 저장

    return article_list

def fetch_article_body(link):
    headers = {
        "User-Agent": "Mozilla/5.0",
    }
    response = requests.get(link, headers=headers)

    if response.status_code != 200:
        print(f"본문 요청 실패: {response.status_code} | 링크: {link}")
        return "본문을 가져올 수 없습니다."

    soup = BeautifulSoup(response.text, 'html.parser')
    body = soup.find('article')  # 본문이 포함된 영역 선택 (네이버 뉴스 기준)
    return body.get_text(strip=True) if body else "본문을 가져올 수 없습니다."

# 현재 날짜를 'yyyymmdd' 형식으로 받아오기
today = datetime.datetime.today().strftime('%Y%m%d')

# 예시 next_value 생성 (시간을 포함)
time_suffix = datetime.datetime.today().strftime('%H%M%S')
next_value = f"{today}{time_suffix}"

print(f"초기 next_value: {next_value}")

# 초기값 설정
all_articles = []
seen_links = set()  # 중복 방지를 위한 링크 저장소
article_count = 0  # 크롤링한 기사 수

# 페이지 크롤링
while article_count < 100:  # 100개 기사를 크롤링
    print(f"크롤링 중: next_value = {next_value}")
    articles = scrape_articles(next_value)
    if articles:
        for article in articles:
            if article[1] not in seen_links:  # 링크가 새로 추가된 경우
                seen_links.add(article[1])
                all_articles.append(article)
                article_count += 1

                if article_count >= 100:
                    print("100개의 기사 크롤링 완료!")
                    break

        # next_value 업데이트 (동적 로직 필요)
        next_value = str(int(next_value) - 10000)  # 예: 감소하는 방식
    else:
        print("더 이상 기사 없음.")
        break

# 결과 출력
for idx, (title, link, date) in enumerate(all_articles, start=1):
    print(f"[{idx}] 제목: {title}")
    print(f"    링크: {link}")
    print(f"    시간: {date}")
    body = fetch_article_body(link)
    print(f"    본문: {body}\n")
