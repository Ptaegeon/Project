import requests
from bs4 import BeautifulSoup
import lxml
import bs4.element
import datetime


def get_soup_obj(url):
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    return soup


def get_top3_news_info(sec, sid):
    default_img = "https://search.naver.com/search.naver?where=image&sm=tab_jum&query=naver#"

    sec_url = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm" \
              + "&sid1=" \
              + sid
    print("section url : ", sec_url)

    soup = get_soup_obj(sec_url)

    news_list3 = []
    lis3 = soup.find('ul', class_='cluster_list').find_all("li", limit=3)
    for li in lis3:
        # title : 뉴스 제목, news_url : 뉴스 URL, image_url : 이미지 URL
        news_info = {
            "title": li.img.attrs.get('alt') if li.img else li.a.text.replace("\n", "").replace("\t", "").replace("\r",
                                                                                                                  ""),
            # "date" : li.find(class_="date").text ,
            "news_url": li.a.attrs.get('href'),
            "image_url": li.img.attrs.get('src') if li.img else default_img
        }
        news_list3.append(news_info)
    return news_list3


def get_news_contents(url):
    soup = get_soup_obj(url)
    body = soup.find('div', class_='go_trans _article_content')
    news_contents = ''
    for content in body:
        if type(content) is bs4.element.NavigableString and len(content) > 50:
            news_contents += content.strip() + ''

    return news_contents


def get_naver_news_top3():
    news_dic = dict()

    sections = ["pol", "eco", "soc"]
    section_ids = ["100", "101", "102"]

    for sec, sid in zip(sections, section_ids):
        news_info = get_top3_news_info(sec, sid)
        print(news_info)

        for news in news_info:
            news_url = news['news_url']
            news_contents = get_news_contents(news_url)

            news['news_contents'] = news_contents
        news_dic[sec] = news_info

    return news_dic


news_dic = get_naver_news_top3()

import gensim

my_section = 'eco'
news_list3 = news_dic[my_section]
for news_info in news_list3:
    try:
        snews_contents = gensim.summarization.summarizer.summarize(news_info['news_contents'], word_count=20)
    except:
        snews_contents = None

    if not snews_contents:
        news_sentences = news_info['news_contents'].split('.')

        if len(news_sentences) > 3:
            snews_contents = '.'.join(news_sentences[:3])
        else:
            snews_contents = '.'.join(news_sentences)

    news_info['snews_contents'] = snews_contents

print("=== 첫번째 뉴스 원문 ===")
print(news_list3[0]['news_contents'])
print("\m=== 첫번째 뉴스  요약문 ===")
print(news_list3[0]['snews_contents'])

import json
import kakao_utils

# token이 저장된 파일
KAKAO_TOKEN_FILENAME = "res/kakao_message/kakao_token.json"
KAKAO_APP_KEY = "b73f63f314870db4afb9a0531fcefd08"
kakao_utils.update_tokens(KAKAO_APP_KEY, KAKAO_TOKEN_FILENAME)

# 사용자가 선택한 카테고리를 제목에 넣기 위한 dictionary
sections_ko = {'pol': '정치', 'eco': '경제', 'soc': '사회'}

# 네이버 뉴스 URL
navernews_url = "https://news.naver.com/main/home.nhn"

# 추후 각 리스트에 들어갈 내용(content) 만들기
contents = []

# 리스트 템플릿 형식 만들기
template = {
    "object_type": "list",
    "header_title": sections_ko[my_section] + " 분야 상위 뉴스 빅3",
    "header_link": {
        "web_url": navernews_url,
        "mobile_web_url": navernews_url
    },
    "contents": contents,
    "button_title": "네이버 뉴스 바로가기"
}
## 내용 만들기
# 각 리스트에 들어갈 내용(content) 만들기
for news_info in news_list3:
    content = {
        "title": news_info.get('title'),
        # "description" : "작성일 : " + news_info.get('date'),
        "image_url": news_info.get('image_url'),
        "image_width": 50, "image_height": 50,
        "link": {
            "web_url": news_info.get('news_url'),
            "mobile_web_url": news_info.get('news_url')
        }
    }

    contents.append(content)

# 카카오톡 메시지 전송
res = kakao_utils.send_message(KAKAO_TOKEN_FILENAME, template)
if res.json().get('result_code') == 0:
    print('뉴스를 성공적으로 보냈습니다.')
else:
    print('뉴스를 성공적으로 보내지 못했습니다. 오류메시지 : ', res.json())
