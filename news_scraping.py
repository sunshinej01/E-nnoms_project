import requests
import datetime
from bs4 import BeautifulSoup
from text_preprocessing import preprocess_text
def scrape_articles(sid, max_articles):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100"
    }
    today = datetime.datetime.today().strftime('%Y%m%d')
    time_suffix = datetime.datetime.today().strftime('%H%M%S')
    next_value = f"{today}{time_suffix}"

    all_articles = []
    seen_links = set()
    article_count = 0

    while article_count < max_articles:
        url = f"https://news.naver.com/section/template/SECTION_ARTICLE_LIST?sid={sid}&sid2=&cluid=&pageNo=1&date=&next={next_value}&_=1736665778225"
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"요청 실패: {response.status_code}")
            break

        temp = response.json()
        html_content = temp['renderedComponent']['SECTION_ARTICLE_LIST']
        soup = BeautifulSoup(html_content, 'html.parser')
        articles = soup.find_all('li', class_='sa_item')

        if not articles:
            print("더 이상 기사 없음.")
            break

        for article in articles:
            title_tag = article.find('a', class_='sa_text_title')
            datetime_tag = article.find(class_='sa_text_datetime')

            if title_tag and datetime_tag:
                title = title_tag.get_text(strip=True)
                link = title_tag.get('href')
                date_str = datetime_tag.get_text(strip=True)

                if link not in seen_links:
                    seen_links.add(link)
                    all_articles.append((title, link, date_str))
                    article_count += 1

                    if article_count >= max_articles:
                        break

        next_value = str(int(next_value) - 10000)

    all_article_bodies = []
    for title, link, _ in all_articles:
        body = fetch_article_body(link)
        preprocessed_body = preprocess_text(body)
        all_article_bodies.append(preprocessed_body)

    return all_articles, all_article_bodies

def fetch_article_body(link):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(link, headers=headers)

    if response.status_code != 200:
        return ""

    soup = BeautifulSoup(response.text, 'html.parser')
    body = soup.find('article')
    return body.get_text(strip=True) if body else ""
