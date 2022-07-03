from archive import get_key_link
import time
from avito_parcer_script import avito_parce_soup, avito_parce
from my_libs.libs_selenium import create_chrome_driver_object
from bs4 import BeautifulSoup
from multiprocessing import Pool
urls = []
outputs = []
item_urls = []
myphones_data = []
def myphones_get_avarage_prices():
    with open('data/myphones.txt', 'r') as f:
        myphones = f.readlines()
    for myphone in myphones:
        key = myphone.split(':')[1]
        key_link = get_key_link(key)
        urls.append(key_link)

    driver = create_chrome_driver_object(headless=True)
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

    for i in range(len(urls)):
        return f'{myphones[i].split(":")[0]}, - {prices[i]}"/"{int(int(prices[i])*float(myphones[i].split(":")[2]))}'

    driver.quit()

#     with open('data/myphones.txt', 'r') as f:
#         myphones = f.readlines()
#     for myphone in myphones:
#         key = myphone.split(':')[1]
#         key_link = get_key_link(key)
#         urls.append(key_link)
#     p = Pool(processes=len(urls))
#     p.map(avito_parce, urls)


