### 필요한 라이브러리
from google_auth_oauthlib.flow import InstalledAppFlow
# 구글 캘린더 API 서비스 객체 생성
from googleapiclient.discovery import build
import datetime

# 구글 클라우드 콘솔에서 다운받은 OAuth 2.0 클라이언트 파일 경로
creds_filename = 'res/smart_scheduler/google_token.json'
# 사용 권한 지정
# https://www.googleapis.com/auth/calendar 캘린더 읽기/쓰기 권한
# https://www.googleapis.com/auth/calendar.readonly 캘린더 읽기 권한
SCOPES = ['https://www.googleapis.com/auth/calendar']

# 파일에 담긴 인증 정보로 구글 서버에 인증하기
# 새 창이 열리면서 구글 로그인 및 정보 제공 동의 후 최종 인증이 완료됩니다.
flow = InstalledAppFlow.from_client_secrets_file(creds_filename, SCOPES)
creds = flow.run_local_server(port=0)

### 객체 생성
service = build('calendar', 'v3', credentials=creds)

# 조회에 사용될 요청 변수 지정
calendar_id = 'primary'  # 사용할 캘린더 ID
today = datetime.date.today().strftime("%Y-%m-%d")  # 일정을 조회할 날짜 YYYY-mm-dd 포맷
time_min = today + 'T00:00:00+09:00'  # 일정을 조회할 최소 날짜
time_max = today + 'T23:59:59+09:00'  # 일정을 조회할 최대 날짜
max_results = 5  # 일정을 조회할 최대 개수
is_single_events = True  # 반복 일정의 여부
orderby = 'startTime'  # 일정 정렬

# 오늘 일정 가져오기
events_result = service.events().list(calendarId=calendar_id,
                                      timeMin=time_min,
                                      timeMax=time_max,
                                      maxResults=max_results,
                                      singleEvents=is_single_events,
                                      orderBy=orderby).execute()

items = events_result.get('items')
print("===== [일정 목록 출력]=====")
print(items)
item = items[0]  # 테스트를 위해 오늘 일정에서 한 개만 가져옵니다.

# 일정 제목
gsummary = item.get('summary')

# 일정 제목에서 [식사-국민대]에서 카테고리와 장소를 추출합니다.
gcategory, glocation = gsummary[gsummary.index('[') + 1: gsummary.index(']')].split('-')

# 구글 캘린더 일정이 연결되어있는 링크입니다.
gevent_url = item.get('htmlLink')

print("\n\n===== [일정 상세 정보 출력]=====")
print("category : ", gcategory)
print("location : ", glocation)
print("event_url : ", gevent_url)

import requests

# 네이버 애플리케이션의 client_id와 client_secret 키 설정
headers = {
    "X-Naver-Client-Id": "Uns3OnBgtkoNvZ1Asv3K",
    "X-Naver-Client-Secret": "TygMM7cwVD"
}

# 지역 검색 요청 파라미터 설정
query = glocation + " 맛집"
params = {
    "sort": "comment",
    "query": query,
    "display": 3
}

# 지역 검색 URL과 요청 파라미터
naver_local_url = "https://openapi.naver.com/v1/search/local.json"

# 지역 검색 요청
res = requests.get(naver_local_url, headers=headers, params=params)

# 지역 검색 결과 확인
places = res.json().get('items')
print(places)

import kakao_utils

KAKAO_TOKEN_FILENAME = 'res/kakao_message/kakao_token.json'
KAKAO_APP_KEY = "b73f63f314870db4afb9a0531fcefd08"
kakao_utils.update_tokens(KAKAO_APP_KEY, KAKAO_TOKEN_FILENAME)

# 일정 주소 네이버 연결할 링크입니다.
gaddr_url = "https://search.naver.com/search.naver?query=" + glocation + " 맛집"
# contents 변수를 초기화 합니다.
contents = []

# 카카오톡 리스트 템플릿을 작성해봅니다.
template = {
    "object_type": "list",
    "header_title": gsummary + " - 맛집 추천",
    "header_link": {
        "web_url": gevent_url,
        "mobile_web_url": gevent_url
    },
    "contents": contents,
    "buttons": [
        {
            "title": "일정 자세히 보기",
            "link": {
                "web_url": gevent_url,
                "mobile_web_url": gevent_url
            }
        },
        {
            "title": "일정 장소 보기",
            "link": {
                "web_url": gaddr_url,
                "mobile_web_url": gaddr_url
            }
        }
    ],
}

# 카카오톡 리스트 템플릿의 contents를 구성합니다.
for place in places:
    ntitle = place.get('title')  # 장소 이름
    ncategory = place.get('category')  # 장소 카테고리
    ntelephone = place.get('telephone')  # 장소 전화번호
    nlocation = place.get('address')  # 장소 지번 주소

    # 각 장소를 클릭할 때 네이버 검색으로 연결해주기 위해 작성된 코드
    query = nlocation + ' ' + ntitle

    # 장소 카테고리가 카페이면 카페 이미지
    # 이외에는 음식 이미지
    if '카페' in ncategory:
        image_url = "https://freesvg.org/img/pitr_Coffee_cup_icon.png"
    else:
        image_url = "https://freesvg.org/img/bentolunch.png?w=150&h=150&fit=fill"

    # 전화번호가 있다면 제목과 함께 넣어줍니다.
    if ntelephone:
        ntitle = ntitle + "\ntel) " + ntelephone

    # 카카오톡 리스트 템플릿 형식에 맞춰줍니다.
    content = {
        "title": "[" + ncategory + "] " + ntitle,
        "description": ' '.join(nlocation.split()[1:]),
        "image_url": image_url,
        "image_width": 50, "image_height": 50,
        "link": {
            "web_url": "https://search.naver.com/search.naver?query=" + query,
            "mobile_web_url": "https://search.naver.com/search.naver?query=" + query
        }
    }
    contents.append(content)

# 카카오톡 메시지 전송
res = kakao_utils.send_message(KAKAO_TOKEN_FILENAME, template)
if res.json().get('result_code') == 0:
    print('일정 맞춤 맛집을 성공적으로 보냈습니다.')
else:
    print('일정 맞춤 맛집을 성공적으로 보내지 못했습니다. 오류메시지 : ', res.json())
