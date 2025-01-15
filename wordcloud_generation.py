from wordcloud import WordCloud
import matplotlib.pyplot as plt
import platform
import os
import io
import base64

# 환경에 맞는 폰트 경로를 자동으로 설정하는 함수
def get_font_path():
    system = platform.system()  # 운영 체제 판별
    if system == "Windows":
        return "C:\\Windows\\Fonts\\SeoulNamsanB.ttf"  # Windows에서 사용할 한글 폰트
    elif system == "Darwin":  # macOS
        # macOS에서 사용할 한글 폰트 (경로에 따라 다를 수 있음)
        if os.path.exists("/Library/Fonts/AppleGothic.ttf"):
            return "/Library/Fonts/AppleGothic.ttf"
        elif os.path.exists("/System/Library/Fonts/AppleGothic.ttf"):
            return "/System/Library/Fonts/AppleGothic.ttf"
        else:
            # NanumGothic이 있을 경우 사용 (별도의 설치가 필요할 수 있음)
            return "/Library/Fonts/NanumGothic.ttf"  # 예시로 NanumGothic을 사용
    else:  # Linux
        # Linux에서 사용할 폰트 (NanumGothic)
        return "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"  # 예시로 NanumGothic을 사용

# 워드클라우드 이미지 생성 함수 (이미지 파일로 반환)
def create_wordcloud(word_freq):
    font_path = get_font_path()  # 환경에 맞는 폰트 경로 가져오기
    wordcloud = WordCloud(font_path=font_path, width=800, height=400, background_color='white', colormap='magma').generate_from_frequencies(word_freq)
    
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
