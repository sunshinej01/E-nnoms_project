import streamlit as st
from news_scraping import scrape_articles
from topic_modeling import lda_topic_modeling
from collections import Counter
from wordcloud_generation import create_wordcloud, get_related_articles
import platform

# 뉴스 소스 ID와 이름 매핑
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

# 환경에 맞는 폰트 설정 함수
def get_font_path():
    system = platform.system()
    if system == 'Windows':
        return "C:\\Windows\\Fonts\\SeoulNamsanB.ttf"
    elif system == 'Darwin':  # macOS
        return "/System/Library/Fonts/AppleGothic.ttf"
    else:  # Linux or others
        return "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# 워드클라우드 생성 및 데이터 저장
def display_wordcloud(category, num_articles):
    sid = news_sources[category]
    articles, article_bodies = scrape_articles(sid, num_articles)

    topics = lda_topic_modeling(article_bodies, num_topics=DEFAULT_NUM_TOPICS, top_n_per_topic=DEFAULT_TOP_N_PER_TOPIC)
    topic_words = [word for words in topics.values() for word in words]
    topic_word_freq = Counter(topic_words)

    wordcloud_freq = Counter({word: topic_word_freq[word] for word in topic_word_freq})
    wordcloud_img = create_wordcloud(wordcloud_freq)

    # 상태에 데이터 저장
    st.session_state.wordcloud_data = {
        "category": category,
        "num_articles": num_articles,
        "image": wordcloud_img,
        "topics": topics,
        "articles": articles,
        "article_bodies": article_bodies,
        "word_freq": wordcloud_freq
    }

# 관련 기사 표시
def display_related_articles():
    data = st.session_state.get("wordcloud_data")
    if data is None:
        return

    sorted_keywords = sorted(data["word_freq"].items(), key=lambda x: x[1], reverse=True)[:DEFAULT_TOP_N_KEYWORDS]
    seen_articles = set()

    for word, _ in sorted_keywords:
        related_articles = get_related_articles(word, data["articles"], data["article_bodies"], seen_articles)
        st.write(f"## {word}")
        if related_articles:
            for title, link, date in related_articles:
                st.write(f"- [{title}]({link}) ({date})")
        else:
            st.write("- 관련 기사가 없습니다.")

# 페이지 렌더링 처리
def render_page():
    # 기본값 설정
    if "category" not in st.session_state:
        st.session_state["category"] = "정치"  # 기본값은 정치
    if "num_articles" not in st.session_state:
        st.session_state["num_articles"] = 30  # 기본값은 30

    # 카테고리와 기사 수 선택
    col1, col2, col3 = st.columns([2, 3, 1])
    with col1:
        category_input = st.selectbox(
            "",  # 라벨 비활성화
            list(news_sources.keys()),
            index=list(news_sources.keys()).index(st.session_state["category"]),
            key="category_input",  # 키 변경
            label_visibility="collapsed"
        )
    with col2:
        num_articles_input = st.number_input(
            "",  # 라벨 비활성화
            min_value=1,
            value=st.session_state["num_articles"],
            key="num_articles_input",  # 키 변경
            label_visibility="collapsed"
        )
    with col3:
        analyze_button = st.button("분석 시작", use_container_width=True)

    # 초기값을 "정치"와 "30"으로 설정하여 첫 워드클라우드 생성
    if "initialized" not in st.session_state:
        # 초기 워드클라우드 생성 및 표시
        st.session_state.initialized = True
        with st.spinner("초기 워드클라우드 생성 중..."):
            display_wordcloud(st.session_state["category"], st.session_state["num_articles"])

    # 분석 버튼 클릭 시 새로운 워드클라우드 생성
    if analyze_button:
        # 분석 시작 버튼 클릭 시 세션 상태 값 업데이트
        st.session_state["category"] = category_input
        st.session_state["num_articles"] = num_articles_input
        with st.spinner("분석 진행 중..."):
            display_wordcloud(category_input, num_articles_input)

    # 기존 워드클라우드 표시
    if "wordcloud_data" in st.session_state and st.session_state.wordcloud_data:
        # 제목을 워드클라우드 바로 위에 표시
        category = st.session_state.get("category")
        num_articles = st.session_state.get("num_articles")
        st.title(f"{category} 분야 뉴스 {num_articles}개 기사 분석")  # 제목 업데이트
        st.image(st.session_state.wordcloud_data["image"], use_column_width=True)

        # 관련 기사 표시
        display_related_articles()

# 메인 실행
if __name__ == "__main__":
    render_page()
