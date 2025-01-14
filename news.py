import streamlit as st
from news_scraping import scrape_articles
from topic_modeling import lda_topic_modeling
from collections import Counter
from wordcloud_generation import create_wordcloud, get_related_articles

# 뉴스 소스 ID와 이름 매핑 (IT/과학까지만 표시)
news_sources = {
    "정치": 100,
    "경제": 101,
    "사회": 102,
    "생활문화": 103,
    "세계": 104,
    "IT/과학": 105
}

# 기본값 설정
DEFAULT_TOP_N_WORDS = 5
DEFAULT_NUM_TOPICS = 5
DEFAULT_TOP_N_PER_TOPIC = 5
DEFAULT_TOP_N_KEYWORDS = 5

# 스트림릿 UI 처리
def run_streamlit():
    st.title("뉴스 기사 분석")

    # 한 줄에 카테고리 선택, 크롤링할 기사 수 입력, 분석 시작 버튼 배치
    col1, col2, col3 = st.columns([2, 3, 1])  # 각 컬럼의 크기를 조절
    with col1:
        source = st.selectbox("뉴스 카테고리", list(news_sources.keys()), key="category", label_visibility="collapsed")  # 라벨만 숨기기
    with col2:
        max_articles = st.number_input("크롤링할 기사 수", min_value=1, value=50, key="num_articles", label_visibility="collapsed")  # 라벨만 숨기기
    with col3:
        analyze_button = st.button("분석 시작", use_container_width=True)  # 버튼 크기 조정

    # 각 요소의 높이를 맞추기 위해 동일한 높이로 설정
    col1.write("")  # 첫 번째 컬럼에 내용이 없으면 높이를 맞추기 위해 공백 추가
    col2.write("")  # 두 번째 컬럼에 내용이 없으면 높이를 맞추기 위해 공백 추가
    col3.write("")  # 세 번째 컬럼에 내용이 없으면 높이를 맞추기 위해 공백 추가

    # 분석 버튼 클릭 후 결과 영역을 분리하여 표시
    if analyze_button:
        # 초기 워드클라우드 생성이 진행 중이면 강제로 중단하고 분석을 바로 시작하도록 함
        if "initialized" in st.session_state and st.session_state.initialized:
            st.session_state.initialized = False  # 초기화 상태를 False로 설정하여 중단시킴

        with st.spinner("분석 진행 중..."):
            sid = news_sources[source]  # 선택된 카테고리의 ID
            # 뉴스 크롤링
            articles, article_bodies = scrape_articles(sid, max_articles)

            # LDA 토픽 모델링
            topics = lda_topic_modeling(article_bodies, num_topics=DEFAULT_NUM_TOPICS, top_n_per_topic=DEFAULT_TOP_N_PER_TOPIC)

            # 토픽에서 단어 추출
            topic_words = [word for words in topics.values() for word in words]
            topic_word_freq = Counter(topic_words)

            # 워드클라우드 생성
            wordcloud_freq = Counter({word: topic_word_freq[word] for word in topic_word_freq})
            wordcloud_img = create_wordcloud(wordcloud_freq)

            # Streamlit에서 이미지를 표시
            st.image(wordcloud_img, use_column_width=True)

            # 상위 N개의 키워드 추출
            sorted_keywords = sorted(wordcloud_freq.items(), key=lambda x: x[1], reverse=True)[:DEFAULT_TOP_N_KEYWORDS]

            # 연관 기사 추출
            seen_articles = set()
            for word, _ in sorted_keywords:
                related_articles = get_related_articles(word, articles, article_bodies, seen_articles)
                st.write(f"## {word}")
                if related_articles:
                    for title, link, date in related_articles:
                        st.write(f"{title}         \n{link} - {date}")
                else:
                    st.write(f"  - 관련 기사가 없습니다.")

    # 초기화 체크
    if "initialized" not in st.session_state:
        st.session_state.initialized = True  # 초기화 여부 체크

        with st.spinner("초기 워드클라우드 생성 중..."):
            # 정치 카테고리의 50개 기사를 크롤링하여 워드클라우드를 생성
            articles, article_bodies = scrape_articles(news_sources["정치"], 50)

            # LDA 토픽 모델링
            topics = lda_topic_modeling(article_bodies, num_topics=DEFAULT_NUM_TOPICS, top_n_per_topic=DEFAULT_TOP_N_PER_TOPIC)
            topic_words = [word for words in topics.values() for word in words]
            topic_word_freq = Counter(topic_words)

            wordcloud_freq = Counter({word: topic_word_freq[word] for word in topic_word_freq})

            # 워드클라우드 생성
            wordcloud_img = create_wordcloud(wordcloud_freq)
            st.image(wordcloud_img, use_column_width=True)

# 메인 실행
if __name__ == "__main__":
    run_streamlit()
