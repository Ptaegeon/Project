import kakao_utils
import requests

KAKAO_TOKEN_FILENAME = "res/kakao_message/kakao_token.json"
KAKAO_APP_KEY = "b73f63f314870db4afb9a0531fcefd08"

tokens = kakao_utils.update_tokens(KAKAO_APP_KEY, KAKAO_TOKEN_FILENAME)
kakao_utils.save_tokens(KAKAO_TOKEN_FILENAME, tokens)

template = {
    "object_type": "text",
    "text": "Hello, world",
    "link": {
        "web_url":"https://naver.com"
    },
}

res = kakao_utils.send_message(KAKAO_TOKEN_FILENAME, template)

# 요청에 실패했다면,
if res.status_code != 200:
    print("error! because ", res.json())
else:  # 성공했다면,

    tokens = res.json()
    print(tokens)
