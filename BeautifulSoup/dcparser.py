import requests
import re
from bs4 import BeautifulSoup as bs

LOGIN_INFO = {
    'user_id' : 'kiiren', 
    'password':'12345^',
    's_url' : 'http%3A%2F%2Fgall.dcinside.com',
    'tieup' : '',
    'url' : '',
    'scurity' : False
}
def appendSecurityKey(dict, html):
    return {**dict, **{key : html[key]}}

with requests.Session() as s:
    first_page = s.get('https://dcid.dcinside.com/join/login.php?s_url=http%3A%2F%2Fgall.dcinside.com')
    html = first_page.text
    soup = bs(html, 'html.parser')
    csrf = ''
    for tag in soup.find_all('input',{"name":re.compile(r'\b.{15}\d\b')}):#re.compile(r'\b.{15}\d\b')
        csrf = tag
        
    assert(csrf != '')
    print("csrf:")
    print(csrf)
    print(type(csrf))
    
    LOGIN_INFO = {**LOGIN_INFO, **{str(csrf) : csrf['value']}}
    #python3 dict concat + {**dict1, **dict2}

    login_req = s.post('https://dcid.dcinside.com/join/member_check.php', data=LOGIN_INFO)
    print(login_req.status_code)
