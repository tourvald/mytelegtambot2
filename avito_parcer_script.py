import time
import lxml
import random
import unidecode
import datetime
from archive import archive, load_archive, get_last_date
from bs4 import BeautifulSoup
from my_libs.libs_selenium import create_chrome_driver_object
import mylibs
from archive import get_key_link
from my_libs.libs_google_sheets import get_myphones_spreadsheet, get_mysells_spreadsheet
from selenium import webdriver
from mylibs import get_bs4_from_driver
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
    av_price = f'{av_price_std}'
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
    print (f'Мои прокси - {proxies}')
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
    print(av_price_std)
    return av_price_std, search_request.lower()

def avito_auto_parce_soup(soup):
    price_list = []
    search_request = soup.find('input', {'data-marker': 'search-form/suggest'}).get('value')  # Название запроса
    div_catalog_serp = soup.find('div', {'data-marker': 'catalog-serp'})  # Выделяем блок в котором хранятся все цены
    for price in div_catalog_serp.find_all('meta', {'itemprop': 'price'}):  # Перебираем подблоки блока div_catalog_serp
        price_list.append(price.get('content'))  # Достаем из них цены и добавляем в список цен
    av_price_std = mylibs.av_price_auto(price_list)
    print(av_price_std)
    return av_price_std, search_request.lower()

def myphones_get_avarage_prices_old():

    urls =[]
    values = get
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

def myphones_get_avarage_prices():
    sum_av_price = 0
    sum_sell_price = 0
    with open('data/checked_proxies.txt', 'r', encoding='UTF-8') as f:
        proxies = f.readlines()
    print(proxies)
    proxies.reverse()
    proxy_cycle = 0
    driver = create_chrome_driver_object(proxy=proxies[proxy_cycle])
    return_ = []
    myphones = get_myphones_spreadsheet()
    for myphone in myphones['values']:
        key = myphone[1]
        key_link = myphone[3]
        index = myphone[2]
        driver.get(key_link)
        contents = driver.page_source
        soup = (BeautifulSoup(contents, 'lxml'))
        av_price, key = avito_parce_soup(soup)
        sellprice = int(int(av_price) * float(myphone[2]))
        return_.append(f'{myphone[0]}, - {av_price}"/"{sellprice}')
        sum_av_price += av_price
        sum_sell_price += sellprice
    return_.append(f'Средняя цена -  {sum_av_price}')
    return_.append(f'Примерная цена продажи -  {sum_sell_price}')
    return return_

def parce_page(driver, url):
    result = []
    soup = get_bs4_from_driver(driver,url)
    name = soup.find('span', {'data-marker': 'item-view/title-info'})
    price = soup.find('span', {'itemprop': 'price'})
    result.append(name.text)
    result.append(unidecode.unidecode(price.text))
    return result


def update_archive(amount_of_keys:int):
    amount = 0
    arch = load_archive()
    for key in arch:
        date = get_last_date(key)
        timedelta = (datetime.datetime.today() - datetime.datetime.strptime(date, '%Y-%m-%d')).days

        if  timedelta > 14:
            url = get_key_link(key)
            print('Ссылка = ',url)
            try:
                soup = get_soup_for_avito_parce(url)
                av_price_std = avito_parce_soup(soup)
                archive(datetime.date.today(), url, av_price_std, key)
                amount +=1
                time.sleep(random.uniform(1,10))
            except Exception as e:
                print (e)
        if amount == amount_of_keys:
            break

if __name__ == "__main__":
    update_archive(5)