from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
import base64

# 워드클라우드 이미지 생성 함수 (plt.show() 대신 이미지를 반환)
def create_wordcloud(word_freq):
    wordcloud = WordCloud(font_path="C:\\Windows\\Fonts\\SeoulNamsanB.ttf", width=800, height=400, background_color='white', colormap='magma').generate_from_frequencies(word_freq)
    
    # 이미지를 메모리 버퍼에 저장
    img = io.BytesIO()
    wordcloud.to_image().save(img, format='PNG')
    img.seek(0)
    
    # 이미지 파일을 base64 인코딩하여 스트림릿에 표시
    img_b64 = base64.b64encode(img.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{img_b64}"

# 관련 기사 출력 함수 (리턴하는 형태로 수정)
def get_related_articles(word, articles, article_bodies, seen_articles, top_n=3):
    related_articles = []

    for i, (title, link, date) in enumerate(articles):
        body = article_bodies[i]
        
        # 이미 출력한 기사는 제외
        if body and word in body and link not in seen_articles:
            related_articles.append((title, link, date))
            seen_articles.add(link)

        if len(related_articles) >= top_n:
            break

    # 관련 기사가 없을 경우, 이미 출력한 기사 중 하나를 출력
    if len(related_articles) == 0:
        for i, (title, link, date) in enumerate(articles):
            body = article_bodies[i]
            # 이미 출력한 기사는 제외
            if body and word in body:
                related_articles.append((title, link, date))
                break

    return related_articles
