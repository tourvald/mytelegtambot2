from my_libs.libs_selenium import create_chrome_driver_object
import time
import lxml
from bs4 import BeautifulSoup
def parce_text_from_yes_links():
    with open('data/neuro_learn/yes_links.txt', 'r', encoding='utf-8') as f:
        links = f.readlines()
    driver = create_chrome_driver_object(proxy='79.140.29.22:80')
    for link in links:
        print(link)
        driver.get(link)
        for i in range (5):
            try:
                contents = driver.page_source
                soup = (BeautifulSoup(contents, 'lxml'))
                print (soup.title)
                break
            except Exception:
                time.sleep(3 * i)
                driver.refresh()
                print('Нихуя не вышло, ждем')


        break
parce_text_from_yes_links()