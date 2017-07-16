from selenium import webdriver
from bs4 import BeautifulSoup
from getpass import getpass
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ACCOUNT = open(os.path.join(BASE_DIR, 'config.json')).read()
data = json.loads(ACCOUNT)
print(data)

driver = webdriver.Chrome(os.path.join(BASE_DIR, 'chromedriver.exe'))

#url에 접근한다.
driver.get('https://nid.naver.com/nidlogin.login')
driver.find_element_by_name('id').send_keys(data['naverid'])
print("Enter Password of " + data['naverid'] +": ")
driver.find_element_by_name('pw').send_keys(getpass())
#Presses Login Button.
driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input').click()
driver.get('https://order.pay.naver.com/home')
html = driver.page_source # get all elements
soup = BeautifulSoup(html, 'html.parser')
notices = soup.select('div.p_inr > div.p_info > a > span')

for n in notices:
    print(n.text.strip())

