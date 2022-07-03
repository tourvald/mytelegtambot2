import time
import lxml
import random
import datetime
from archive import archive
from bs4 import BeautifulSoup
from my_libs.libs_selenium import create_chrome_driver_object
import mylibs
from archive import get_key_link
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC




def avito_parce(url):
    print (url)
    driver = create_chrome_driver_object()
    driver.get(url)
    time.sleep(3)
    for i in range(5):
        try:
            contents = driver.page_source
            soup = BeautifulSoup(contents, 'lxml')
            search_request = soup.find('input', {'data-marker': 'search-form/suggest'}).get('value')  # Название запроса
            break
        except Exception as e:
            driver.refresh()
            print ('Ждем 5 сек')
            time.sleep(5)
            print (e)
    price_list = []
    div_catalog_serp = soup.find('div', {'data-marker': 'catalog-serp'})  # Выделяем блок в котором хранятся все цены
    for price in div_catalog_serp.find_all('meta', {'itemprop': 'price'}):  # Перебираем подблоки блока div_catalog_serp
        price_list.append(price.get('content'))  # Достаем из них цены и добавляем в список цен
    av_price_std = mylibs.av_price_sdt(price_list)
    av_price_old = mylibs.av_price_old(price_list)
    av_price = f'{av_price_old}, {av_price_std}'
    print(av_price_old, av_price_std)
    archive(datetime.date.today(), url, av_price, search_request.lower())
    return av_price_std, search_request.lower()

def get_soup_for_avito_parce_old(url):
    with open('data/checked_proxies.txt', 'r', encoding='UTF-8') as f:
        proxies = f.readlines()
    print (proxies)
    proxies.reverse()
    proxy_cycle = 0
    retryes = 0
    len_proxies = len(proxies)
    driver = create_chrome_driver_object(proxy=proxies[proxy_cycle])
    while proxy_cycle != 2:
        retryes += 1
        try:
            driver.get(url)
            driver.implicitly_wait(10)
        except Exception as e:
            print(e.__cause__)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        if not soup.title:
            print(f'Cуп не получен, попытка {retryes}, ждем  {delay * retryes} сек')
            if retryes == 7:
                retryes = 0
                driver.close()
                count_proxies += 1
                if count_proxies > len_proxies:
                    count_proxies = 0
                    proxy_cycle += 1
                    print(f'Загрузка не удалась. Попыток - {retryes}')
                driver = create_chrome_driver_object(proxy=proxies[count_proxies])
            continue

        if soup.title.text == 'Доступ временно заблокирован':
            print(soup.title.text)
            driver.close()
            count_proxies += 1
            if count_proxies > len_proxies:
                count_proxies = 0
                proxy_cycle += 1
                print(f'Загрузка не удалась. Попыток - {retryes}')
            driver = create_chrome_driver_object(proxy=proxies[count_proxies])
            delay = random.uniform(3, 6)
            time.sleep(delay)
            continue
        else:
            break
    return soup

def get_soup_for_avito_parce(url):
    with open('data/checked_proxies.txt', 'r', encoding='UTF-8') as f:
        proxies = f.readlines()
    print (proxies)
    proxies.reverse()
    proxy_cycle = 0
    retryes = 0
    len_proxies = len(proxies)
    driver = create_chrome_driver_object(proxy=proxies[proxy_cycle])
    while proxy_cycle != 2:
        retryes += 1
        try:
            driver.get(url)
            d = WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located(
                    (By.TAG_NAME, 'body')
                )
            )
            print (f'Good = {d}')
        except Exception as e:
            print(e)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        if not soup.title:
            print(f'Cуп не получен, попытка {retryes}, ждем  {delay * retryes} сек')
            if retryes == 7:
                retryes = 0
                driver.close()
                count_proxies += 1
                if count_proxies > len_proxies:
                    count_proxies = 0
                    proxy_cycle += 1
                    print(f'Загрузка не удалась. Попыток - {retryes}')
                driver = create_chrome_driver_object(proxy=proxies[count_proxies])
            continue

        if soup.title.text == 'Доступ временно заблокирован':
            print(soup.title.text)
            driver.close()
            count_proxies += 1
            if count_proxies > len_proxies:
                count_proxies = 0
                proxy_cycle += 1
                print(f'Загрузка не удалась. Попыток - {retryes}')
            driver = create_chrome_driver_object(proxy=proxies[count_proxies])
            delay = random.uniform(3, 6)
            time.sleep(delay)
            continue
        else:
            break
    return soup

def avito_parce_soup(soup):
    price_list = []
    search_request = soup.find('input', {'data-marker': 'search-form/suggest'}).get('value')  # Название запроса
    div_catalog_serp = soup.find('div', {'data-marker': 'catalog-serp'})  # Выделяем блок в котором хранятся все цены
    for price in div_catalog_serp.find_all('meta', {'itemprop': 'price'}):  # Перебираем подблоки блока div_catalog_serp
        price_list.append(price.get('content'))  # Достаем из них цены и добавляем в список цен
    av_price_std = mylibs.av_price_sdt(price_list)
    av_price_old = mylibs.av_price_old(price_list)
    print(av_price_old, av_price_std)
    return av_price_std, search_request.lower()

def myphones_get_avarage_prices():

    urls =[]
    with open('/Users/dmitry/Desktop/mytelegtambot2/data/myphones.txt', 'r') as f:
        myphones = f.readlines()
    for myphone in myphones:
        key = myphone.split(':')[1]
        key_link = get_key_link(key)
        urls.append(key_link)

    with open('data/checked_proxies.txt', 'r', encoding='UTF-8') as f:
        proxies = f.readlines()
    print(proxies)
    proxies.reverse()
    proxy_cycle = 0
    retryes = 0
    len_proxies = len(proxies)
    driver = create_chrome_driver_object(proxy=proxies[proxy_cycle])
    for url in urls:
        driver.get(url)
        time.sleep(1)
        if url == urls[-1]:
            break
        driver.switch_to.new_window()
    time.sleep(3)
    prices = []
    for i in range(len(urls)):
        driver.switch_to.window(driver.window_handles[i])
        contents = driver.page_source
        soup = (BeautifulSoup(contents, 'lxml'))
        av_price, key = avito_parce_soup(soup)
        prices.append(av_price)
    return_ = []
    myprices = []
    for i in range(len(urls)):
        myprice = int(int(prices[i])*float(myphones[i].split(":")[2]))
        myprices.append(myprice)
        return_.append(f'{myphones[i].split(":")[0]}, - {prices[i]}"/"{myprice}')
    return_.append(f'Средняя цена -  {sum(prices)}')
    return_.append(f'Примерная цена продажи -  {sum(myprices)}')
    return return_
