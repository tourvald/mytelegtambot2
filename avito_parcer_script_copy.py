from statistics import mean
import numpy as np
import requests
import re
import time
import lxml
import random
import json
import datetime
from archive import archive
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import mylibs
from selenium.webdriver.chrome.options import Options



def avito_parce(url):

    print (f'Начинаем парсинг', end = '; ')

    with open('settings/bot_settings.json', 'r', encoding='utf-8') as f:
        bot_settings = json.loads(f.read())
        f.close() #Закрываем файл
    print (f'archive_link={bot_settings["archive_link"]}',end = '; ')
    print(f'pages_to_parce={bot_settings["pages_to_parce"]}',end = '; ')
    wl, pagination_list, price_list = [], [], []
    headers = {
        "Accept": "*/*",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/98.0.4758.80 YaBrowser/22.1.0 Yowser/2.5 Safari/537.36"
    }
    print(f'parce_mode={bot_settings["parce_mode"]}', end=' ')
    if bot_settings["parce_mode"] == "requests":
        contents = requests.get(url, headers=headers).content
    elif "selenium":
        print ('Запускаем selenium')
        with open('settings/webdriver.txt', 'r', encoding='utf-8') as f:
            web_driver = f.readline()
            f.close() #Закрываем файл
        chromeOptions = selenium.webdriver.ChromeOptions()                       #Отключаем
        prefs = {"profile.managed_default_content_settings.images":2}   #Загрузку
        chromeOptions.page_load_strategy='eager'
        chromeOptions.add_experimental_option("prefs",prefs)
        chromeOptions.add_argument('headless')
        chromeOptions.add_argument("--ignore-ssl-errors")
        chromeOptions.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
        chromeOptions.add_argument("--disable-blink-features=AutomationControlled")#Картинок
        chromeOptions.add_argument("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 YaBrowser/21.3.3.230 Yowser/2.5 Safari/537.36")
        s = Service(executable_path=web_driver)
        driver = webdriver.Chrome(service=s, options=chromeOptions)
        driver.get(url)

        print('Загрузили url', end=' ')
        time.sleep(random.uniform(1, 3))
        contents = driver.page_source

    soup = BeautifulSoup(contents, "lxml")
    search_request = soup.find('input', {'data-marker': 'search-form/suggest'}).get('value') #Название запроса
    div_catalog_serp = soup.find('div',{'data-marker': 'catalog-serp'})  # Выделяем блок в котором хранятся все цены
    for price in div_catalog_serp.find_all('meta', {'itemprop': 'price'}):  # Перебираем подблоки блока div_catalog_serp
        price_list.append(price.get('content'))  # Достаем из них цены и добавляем в список цен
    for i in soup.find_all("a", {"class": "pagination-page"}): #Перебираем блоки с ссылками на доп страницы
        pagination_list.append(f'https://www.avito.ru{i.get("href")}') #Добавляем из каждого блока ссылку в список
    print ('Количество страниц = ', len(pagination_list))

    pags = 1
    if len(pagination_list) > 1 and bot_settings["pages_to_parce"] > 1: #Если количество ссылок больше двух то удаляем первую и последнюю
        del pagination_list[0]
        # del pagination_list[-1]  # последняя всегда дубликат. Удаляем.
        for pagination in pagination_list: #Парсим оставшиеся ссылки
            if pags >= bot_settings["pages_to_parce"]:      #Прервать цикс и не парсить больше доп ссылки, если спаршено X допстраниц
                break           #0 - Не парсить доп страницы вообще.
            if bot_settings["parce_mode"] == "requests":
                contents = requests.get(pagination).content
            elif "selenium":
                print(f'selenium:{pagination}')
                driver.get(pagination)
                time.sleep(random.uniform(1, 3))
                contents = driver.page_source

                soup = BeautifulSoup(contents, 'lxml')
                div_catalog_serp = soup.find('div', {'data-marker': 'catalog-serp'})
                for price in div_catalog_serp.find_all('meta',{'itemprop': 'price'}):
                    price_list.append(price.get('content'))
                pags = pags + 1
                if pags > bot_settings["pages_to_parce"]:
                    break
    driver.quit()
    av_price_std = mylibs.av_price_sdt(price_list)
    av_price_old = mylibs.av_price_old(price_list)
    av_price = f'{av_price_old}, {av_price_std}'
    print(av_price_old, av_price_std)
    # if bot_settings["archive_link"] == 'Yes':
    archive(datetime.date.today(), url, av_price, search_request.lower())
    return av_price, search_request.lower()

def avito_parce_soup(soup):
    price_list = []
    search_request = soup.find('input', {'data-marker': 'search-form/suggest'}).get('value')  # Название запроса
    div_catalog_serp = soup.find('div', {'data-marker': 'catalog-serp'})  # Выделяем блок в котором хранятся все цены
    for price in div_catalog_serp.find_all('meta', {'itemprop': 'price'}):  # Перебираем подблоки блока div_catalog_serp
        price_list.append(price.get('content'))  # Достаем из них цены и добавляем в список цен
    av_price_std = mylibs.av_price_sdt(price_list)
    av_price_old = mylibs.av_price_old(price_list)
    av_price = f'{av_price_old}, {av_price_std}'
    print(av_price_old, av_price_std)
    return av_price_std, search_request.lower()