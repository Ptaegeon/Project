import requests
from bs4 import BeautifulSoup
import lxml
#
# html_doc = """
# <html><head><title>The Dormouse's story</title></head>
# <body>
# <p class="title"><b>The Dormouse's story</b></p>
#
# <p class="story">Once upon a time there were three little sisters; and their names were
# <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
# <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
# <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
# and they lived at the bottom of a well.</p>
#
# <p class="story">...</p>
# """
#
# soup = BeautifulSoup(html_doc, 'lxml')
# print("soup.body.p 의 결과 : ", soup.body.p)
# print("soup.body.p 의 결과 : ", soup.body.p)
#
# print()

url = "https://movie.naver.com/movie/bi/mi/review.naver?code=191633#"
res = requests.get(url)

soup = BeautifulSoup(res.text, 'lxml')
ul = soup.find('ul',class_="rvw_list_area")
lis = ul.find_all('li')
count = 0
for li in lis :
    count+=1
    print(f"[{count}", li.a.string)