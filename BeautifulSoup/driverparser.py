from selenium import webdriver

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(BASE_DIR, 'result.json'), 'w+') as json_file:
        json.dump(data,json_file)
driver = webdriver.Chrome('')