# parser.py
import requests
from bs4 import BeautifulSoup
import os
# Python이 실행될 때 DJANGO_SETTINGS_MODULE이라는 환경 변수에 현재 프로젝트의 settings.py파일 경로를 등록합니다.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "websaver.settings")
# 이제 장고를 가져와 장고 프로젝트를 사용할 수 있도록 환경을 만듭니다.
import django
django.setup()
#python manage.py shell

def parse_blog():
    req = requests.get('https://beomi.github.io/')
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    my_titles = soup.select(
        'h3 > a'
        )

    data = {}

    for title in my_titles:
        data[title.text] = title.get('href')
    return data

if __name__=='__main__':
    blog_data_dict = parse_blog()
    for t,l in blog_data_dict.items():
        BlogData(title=t, link=l).save()