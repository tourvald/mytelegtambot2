from my_libs.libs_selenium import create_chrome_driver_object
from mylibs import get_bs4_from_driver
import os
# os.chdir('..')
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

if __name__ == "__main__":
    get_price_from_site('https://biggeek.ru/catalog/apple-iphone-14-pro', 'iPhone 14 Pro 256GB')
    get_price_from_site('https://biggeek.ru/catalog/apple-iphone-14-pro-max', '14 Pro Max 128GB')