import time
from bs4 import BeautifulSoup
import requests

def scrape_articles(page_no, next_value):
    # 기본 설정
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100"
    }
    
    # URL 구성
    url = f"https://news.naver.com/section/template/SECTION_ARTICLE_LIST?sid=100&sid2=&cluid=&pageNo={page_no}&date=&next={next_value}&_=1736665778225"
    
    # 요청 보내기
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"페이지 {page_no} 요청 실패: {response.status_code}")
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
        if title_tag:
            title = title_tag.get_text(strip=True)
            link = title_tag.get('href')
            article_list.append((page_no, title, link))
    return article_list

def fetch_article_body(link):
    # 기사 본문 가져오기
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

# 초기값 설정
next_value = "20250111185615"  # 초기 next 값
all_articles = []
seen_links = set()  # 중복 방지를 위한 링크 저장소

# 페이지 크롤링
for page_no in range(1, 6):  # 1~5 페이지 크롤링
    articles = scrape_articles(page_no, next_value)
    if articles:
        new_articles = []
        for article in articles:
            if article[2] not in seen_links:  # 링크가 새로 추가된 경우
                seen_links.add(article[2])
                new_articles.append(article)
        all_articles.extend(new_articles)
        # next_value 업데이트 (여기에 동적 로직 필요)
        next_value = str(int(next_value) - 10000)  # 예: 감소하는 방식
    else:
        break

# 결과 출력
for idx, (page, title, link) in enumerate(all_articles, start=1):
    print(f"[{idx}] (페이지 {page}) 제목: {title}")
    print(f"    링크: {link}")
    body = fetch_article_body(link)
    print(f"    본문: {body}\n")
