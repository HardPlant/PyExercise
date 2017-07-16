from selenium import webdriver
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

driver = webdriver.Chrome(os.path.join(BASE_DIR, 'chromedriver.exe'))

#url에 접근한다.
driver.get('https://google.com')