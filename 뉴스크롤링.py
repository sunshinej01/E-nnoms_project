import re
import requests
import datetime
from bs4 import BeautifulSoup
from konlpy.tag import Okt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# 뉴스 크롤링 함수
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

    # 기사 본문도 함께 크롤링
    all_article_bodies = []
    for title, link, _ in all_articles:
        body = fetch_article_body(link)
        preprocessed_body = preprocess_text(body)
        all_article_bodies.append(preprocessed_body)

    return all_articles, all_article_bodies

# 기사 본문 추출 함수
def fetch_article_body(link):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(link, headers=headers)

    if response.status_code != 200:
        return ""

    soup = BeautifulSoup(response.text, 'html.parser')
    body = soup.find('article')
    return body.get_text(strip=True) if body else ""

# 텍스트 전처리 함수
def preprocess_text(text, custom_stop_words=None):
    okt = Okt()
    base_stop_words = {'은', '는', '이', '가', '을', '를', '에', '의', '와', '과', '도', '으로', '부터', '까지',
                       '더불어', '관련', '대한', '통해', '한다', '한다면', '한다는', '그리고', '또한', '있다', '이후',
                       '라고', '지난해', '가장', '대해', '이번', '대비', '오전', '개월'}

    if custom_stop_words:
        base_stop_words.update(custom_stop_words)

    text = re.sub(r'[^\w\s]', '', text)
    text = text.lower()
    words = okt.nouns(text)
    filtered_words = [word for word in words if word not in base_stop_words and len(word) > 1]

    return ' '.join(filtered_words)

# LDA 토픽 모델링 함수
def lda_topic_modeling(corpus, num_topics=5, top_n_per_topic=5):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)

    lda = LatentDirichletAllocation(n_components=num_topics, random_state=42)
    lda.fit(tfidf_matrix)

    topics = defaultdict(list)
    feature_names = vectorizer.get_feature_names_out()

    for topic_idx, topic in enumerate(lda.components_):
        top_features = [feature_names[i] for i in topic.argsort()[:-top_n_per_topic-1:-1]]
        topics[topic_idx] = top_features

    return topics

# 워드클라우드 생성 함수
def create_wordcloud(word_freq):
    wordcloud = WordCloud(font_path="C:\\Windows\\Fonts\\SeoulNamsanB.ttf", width=800, height=400, background_color='white', colormap='magma').generate_from_frequencies(word_freq)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis('off')
    plt.show()

# 관련 기사 출력 함수 (상위 단어 출력만)
def print_related_articles(word, articles, article_bodies, seen_articles, top_n=3):
    related_articles = []

    for i, (title, link, date) in enumerate(articles):
        body = article_bodies[i]
        
        # 이미 출력한 기사는 제외
        if body and word in body and link not in seen_articles:
            related_articles.append((title, link, date))
            seen_articles.add(link)

        if len(related_articles) >= top_n:
            break

    if related_articles:
        print(f"\n단어: {word}")
        for idx, (title, link, date) in enumerate(related_articles):
            print(f"  {idx + 1}. {title} ({link})")
    else:
        print(f"\n단어: {word}와 관련된 기사가 없습니다.")

# 통합 실행 함수
def main(sid, max_articles, top_n_words, num_topics, top_n_per_topic=5, custom_stop_words=None, top_n_keywords=5):
    print("뉴스 크롤링 중...")
    articles, article_bodies = scrape_articles(sid, max_articles)

    # LDA 토픽 모델링
    print("\nLDA 토픽 모델링 중...")
    topics = lda_topic_modeling(article_bodies, num_topics, top_n_per_topic)

    # 워드클라우드 생성 (토픽별 키워드로)
    print("\n워드클라우드 생성 중...")
    topic_words = [word for words in topics.values() for word in words]
    topic_word_freq = Counter(topic_words)

    # 전체 기사에서 나온 빈도수를 기반으로 워드클라우드 생성
    wordcloud_freq = Counter({word: topic_word_freq[word] for word in topic_word_freq})
    create_wordcloud(wordcloud_freq)

    # 상위 단어 출력
    sorted_keywords = sorted(wordcloud_freq.items(), key=lambda x: x[1], reverse=True)[:top_n_keywords]
    seen_articles = set()  # 이미 출력된 기사 추적

    print("\n[상위 단어와 연관 기사]")
    for word, freq in sorted_keywords:
        print_related_articles(word, articles, article_bodies, seen_articles)

# 실행 예시
if __name__ == "__main__":
    main(
        sid=100,  # 정치 분야
        max_articles=50,  # 최대 기사 수
        top_n_words=5,  # 문서당 주요 단어 수
        num_topics=5,  # 토픽 수
        top_n_per_topic=5,  # 각 토픽에서 추출할 단어 수
        custom_stop_words=None,  # 커스텀 불용어 (필요시 추가)
        top_n_keywords=5  # 출력할 상위 키워드 수
    )
