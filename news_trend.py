import streamlit as st
import time
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from io import BytesIO

def render_page():
    # 세션 상태 초기화
    for key, value in {
        "data": [],
        "message": None,
        "message_time": None,
        "selected_category": "정치",
        "num_articles": 50,
    }.items():
        if key not in st.session_state:
            st.session_state[key] = value

    # 뉴스 크롤링 함수 (샘플 데이터 반환)
    def crawl_news(category, num_articles):
    # 여기에서 실제 크롤링 코드를 작성해야 함
    # 현재는 샘플 데이터로 대체
        return [f"Sample news title {i+1} for {category}" for i in range(num_articles)]

    # 텍스트 전처리 및 워드 클라우드 생성 함수
    def generate_wordcloud(texts):
        text = " ".join(texts)
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
        return wordcloud

    # 워드 클라우드를 파일로 저장하는 함수
    def get_wordcloud_image(wordcloud):
        img = BytesIO()
        wordcloud.to_file(img)
        img.seek(0)
        return img

    st.header("실시간 뉴스 트렌드")

    # 두 개의 컬럼으로 레이아웃 구성
    col1, col2 = st.columns([1, 1])

    # 뉴스 분야 선택 (셀렉트 박스)
    with col1:
        st.selectbox(
        "뉴스 분야를 선택하세요:",
        ["정치", "경제", "사회", "생활/문화", "과학", "세계"],
        key="selected_category",
        )

    # 크롤링할 개수 입력 (오른쪽 컬럼)
    with col2:
        st.number_input(
        "크롤링할 뉴스 개수:", min_value=1, max_value=500, value=50, step=1, key="num_articles"
        )

    # 크롤링 및 분석 버튼
    if st.button("분석 시작", use_container_width=True):
    # 크롤링 실행
        news_titles = crawl_news(st.session_state.selected_category, st.session_state.num_articles)

    # 워드 클라우드 생성
        wordcloud = generate_wordcloud(news_titles)

        col1, col2 = st.columns([6, 1])
        # 워드 클라우드 시각화
        st.subheader("워드 클라우드")
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        st.pyplot(plt)

        # 워드 클라우드 파일 다운로드 기능 추가
        img = BytesIO()
        wordcloud.to_image().save(img, format="PNG")
        img.seek(0)
        st.download_button(
        label="이미지 다운로드",
        data=img,
        file_name="wordcloud.png",
        mime="image/png"
        )

        # 순위별 키워드 표시 (샘플 데이터로 구현)
        st.subheader("순위별 키워드")
        word_freq = {word: len(word) for word in st.session_state.selected_category.split()}
        sorted_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        for i, (word, freq) in enumerate(sorted_keywords[:10], start=1):
            st.write(f"{i}. {word} (Frequency: {freq})")
