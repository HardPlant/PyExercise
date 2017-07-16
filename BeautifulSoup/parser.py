import requests
from bs4 import BeautifulSoup
import json
import os

with requests.Session() as s:
    req = requests.get('https://www.clien.net/service/')

    html = req.text
    header = req.headers
    status = req.status_code
    is_ok = req.ok
    # BeautifulSoup으로 html소스를 python객체로 변환하기
    # 첫 인자는 html소스코드, 두 번째 인자는 어떤 parser를 이용할지 명시.
    # 이 글에서는 Python 내장 html.parser를 이용했다.
    soup = BeautifulSoup(html, 'html.parser')
    my_titles = soup.select(
        'h3 > a'
        )
    data = {}
    # my_titles는 list 객체
    for title in my_titles:
        '''
        # Tag안의 텍스트
        print(title.text)
        # Tag의 속성을 가져오기(ex: href속성)
        print(title.get('href'))
        '''
        data[title.text] = title.get('href')

    with open(os.path.join(BASE_DIR, 'result.json'), 'w+') as json_file:
        json.dump(data,json_file)