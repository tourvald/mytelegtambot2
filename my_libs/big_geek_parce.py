#1) Обработка ссылки на страницу товара
#2) Поддержка сайтов:
    # Avito.ru
    # 77Store.ru
    # Wildberries.ru
    # sotohit.ru
# 3) Алгоритм работы:
#     1 - Определение сайта с которого происходит парсинг
#     2 - Загрузка страницы и и преобразование ее в объект BS4
#     3 - Обработка супа функцией соответствующей адресу сайта
import os

import unidecode

from my_libs.libs_selenium import create_chrome_driver_object
from mylibs import get_bs4_from_driver


def biggeek_parce(url):
    items = []
    driver = create_chrome_driver_object()
    soup = get_bs4_from_driver(driver, url)
    cards = soup.find_all('div', {'class': 'catalog-card'})
    for card in cards:
        item = []
        item.append(card.find('a', {'class': 'catalog-card__title cart-modal-title'}).text)
        item.append(card.find('div', {'class': 'catalog-card__price-row'}).text)
        items.append(item)
    return items

def choose_engine_to_parce(url):
    if 'biggeek' in url:
        return biggeek_parce
    else:
        print('Этот сайт не поддерживается')
        return None


def get_price_from_site(url, name):
    return_ = []
    engine = choose_engine_to_parce(url)
    if engine:
        items = engine(url)
    for item in items:
        if name in item[0]:
            return_.append(item)
    return return_


def page_parce_choose_engine(url):
    if 'biggeek' in url:
        return biggeek_page_parce
    elif 'avito' in url:
        return page_parce_engine_avito
    else:
        print('Этот сайт не поддерживается')
        return None
def page_parce_engine_avito(url, driver):
    item = []
    soup = get_bs4_from_driver(driver,url)
    name = soup.find('span', {'data-marker': 'item-view/title-info'})
    price = soup.find('span', {'itemprop': 'price'})
    item.append(name.text)
    item.append(unidecode.unidecode(price.text))
    return item

def page_parce(url: str, web_driver:object) -> list:
    engine = page_parce_choose_engine(url)
    if engine:
        item = engine(url, web_driver)
    else:
        print('Этот сайт не поддерживается')
        return None

if __name__ == "__main__":
    os.chdir('..')
    driver = create_chrome_driver_object()
    url = 'https://www.avito.ru/moskva/tovary_dlya_detey_i_igrushki/segway_ninebot_f40a_2503909651'
    page_parce(url, driver)