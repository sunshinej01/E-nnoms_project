import re
import requests
import datetime
from bs4 import BeautifulSoup
from konlpy.tag import Okt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from collections import defaultdict
import nltk
import matplotlib.pyplot as plt
from wordcloud import WordCloud

nltk.download('stopwords')
nltk.download('punkt')

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

    return all_articles

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
                       '라고'}

    if custom_stop_words:
        base_stop_words.update(custom_stop_words)

    text = re.sub(r'[^\w\s]', '', text)
    text = text.lower()
    words = okt.nouns(text)
    filtered_words = [word for word in words if word not in base_stop_words and len(word) > 1]

    return ' '.join(filtered_words)

# TF-IDF 분석 및 주요 단어 추출 함수
def compute_tfidf(corpus, top_n=5, custom_stop_words=None):
    vectorizer = TfidfVectorizer(stop_words=custom_stop_words)
    tfidf_matrix = vectorizer.fit_transform(corpus)
    feature_names = vectorizer.get_feature_names_out()

    top_words_per_doc = []
    for doc in tfidf_matrix:
        sorted_indices = doc.toarray().flatten().argsort()[::-1]
        top_words = [feature_names[idx] for idx in sorted_indices[:top_n]]
        top_words_per_doc.append(top_words)

    return top_words_per_doc, feature_names

# 워드클라우드 생성 함수
def create_wordcloud(words_freq):
    # Windows에서 한글이 깨지지 않도록 '맑은 고딕' 폰트 경로를 설정합니다.
    wordcloud = WordCloud(font_path="C:\\Windows\\Fonts\\malgun.ttf", width=800, height=400, background_color='white').generate_from_frequencies(words_freq)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis('off')
    plt.show()

# 토픽 모델링 함수
def topic_modeling(corpus, num_topics=5, top_n_per_topic=5):
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

# 전체 기사에서 LDA 토픽 단어 빈도수를 바탕으로 워드클라우드 생성
def create_combined_wordcloud(topics, all_article_bodies):
    word_freq = defaultdict(int)
    # 전체 기사에서 각 토픽의 주요 단어 빈도를 계산
    for article_body in all_article_bodies:
        for topic_words in topics.values():
            for word in topic_words:
                if word in article_body:
                    word_freq[word] += article_body.count(word)

    # 전체 기사에서 나온 단어들로 워드클라우드 생성
    print("전체 기사 워드클라우드 생성 중...")
    create_wordcloud(word_freq)

# 통합 실행 함수
def main(sid, max_articles, top_n_words, num_topics, top_n_per_topic=5, custom_stop_words=None):
    print("뉴스 크롤링 중...")
    articles = scrape_articles(sid, max_articles)

    all_article_bodies = []
    for title, link, _ in articles:
        body = fetch_article_body(link)
        preprocessed_body = preprocess_text(body, custom_stop_words)
        all_article_bodies.append(preprocessed_body)

    print("TF-IDF 분석 중...")
    top_words_per_doc, feature_names = compute_tfidf(all_article_bodies, top_n_words, custom_stop_words)

    # 토픽 모델링 수행
    print("토픽 모델링 중...")
    topics = topic_modeling([" ".join(top_words) for top_words in top_words_per_doc], num_topics, top_n_per_topic)

    # LDA 결과로 나온 토픽 단어들을 바탕으로 전체 기사 워드클라우드 생성
    create_combined_wordcloud(topics, all_article_bodies)

    # 결과 출력
    print("\n[토픽 모델링 결과]")
    for topic_idx, top_words in topics.items():
        print(f"토픽 {topic_idx + 1}: {', '.join(top_words)}")
        for title, link, _ in articles:
            if any(word in " ".join(top_words) for word in top_words):
                print(f"    - {title} ({link})")

# 실행 예시
if __name__ == "__main__":
    main(
        sid=101,  # 경제 분야
        max_articles=100,  # 최대 50개 기사
        top_n_words=5,  # 문서당 주요 단어 5개
        num_topics=5,  # 3개의 토픽 생성
        top_n_per_topic=5,  # 각 토픽에서 추출할 단어 수
        custom_stop_words=None  # 커스텀 불용어 비워둠
    )
