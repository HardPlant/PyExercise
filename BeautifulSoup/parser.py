import requests
from bs4 import BeautifulSoup
import json
import os
LOGIN_INFO = {
    'userId' : , 
    'userPassword' :
}

with requests.Session() as s:
    req = s.post('https://www.clien.net/service/login', data=LOGIN_INFO)
    print(login_req.status_code)