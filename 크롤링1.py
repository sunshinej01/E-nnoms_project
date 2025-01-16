from bs4 import BeautifulSoup
import requests
headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100"
}
url = "https://news.naver.com/section/template/SECTION_ARTICLE_LIST?sid=100&sid2=&cluid=&pageNo=5&date=&next=20250111185615&_=1736665778225"
response = requests.get(url, headers=headers)
temp = response.json()
a = temp['renderedComponent']['SECTION_ARTICLE_LIST']
soup = BeautifulSoup(a, 'html.parser')

articles = soup.find_all('li', class_='sa_item')

for article in articles:
    title_tag = article.find('a', class_='sa_text_title')
    if title_tag:
        title = title_tag.get_text(strip=True)
        link = title_tag.get('href')
        print(f"제목: {title}")
        print(f"링크: {link}")