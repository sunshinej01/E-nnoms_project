import re
from konlpy.tag import Okt

def preprocess_text(text, custom_stop_words=None):
    okt = Okt()
    base_stop_words = {'은', '는', '이', '가', '을', '를', '에', '의', '와', '과', '도', '으로', '부터', '까지',
                       '더불어', '관련', '대한', '통해', '한다', '한다면', '한다는', '그리고', '또한', '있다', '이후',
                       '라고', '지난해', '가장', '대해', '이번', '대비', '오전', '개월', '각각', '워낙', '통한', '말씀'}

    if custom_stop_words:
        base_stop_words.update(custom_stop_words)

    text = re.sub(r'[^\w\s]', '', text)
    text = text.lower()
    words = okt.nouns(text)
    filtered_words = [word for word in words if word not in base_stop_words and len(word) > 1]

    return ' '.join(filtered_words)
