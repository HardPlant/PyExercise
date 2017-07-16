from selenium import webdriver
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

driver = webdriver.Chrome(os.path.join(BASE_DIR, 'chromedriver.exe'))

#url에 접근한다.
driver.get('https://nid.naver.com/nidlogin.login')

account = open(os.path.join(BASE_DIR, 'config.json')).read()
data = json.loads(account)
print(data)