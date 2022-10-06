import requests
import json

def save_image(image_url, file_name):
    img_response = requests.get(image_url)

    if img_response.status_code == 200:
        with open(file_name,"wb") as fp:
            fp.write(img_response.content)

url = "https://dapi.kakao.com/v2/search/image"
headers = {
    "Authorization" : "KakaoAK b73f63f314870db4afb9a0531fcefd08"
}
data = {
    "query" : "펭수"
}

response = requests.post(url, headers = headers, data=data)

if response.status_code !=200:
    print("error",response.json())
else:
    count=0

    for image_info in response.json()['documents']:
        print(f'[{count}th] image_url =',image_info['image_url'])

        count+=1
        file_name = "test_%d.jpg" %(count)
        save_image(image_info['image_url'],file_name)