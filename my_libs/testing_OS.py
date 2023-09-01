import requests
from bs4 import BeautifulSoup
import os
import lxml
from multiprocessing import Pool
from libs_selenium import create_chrome_driver_object




# req_proxies = {
#   'http': proxies[0],
#   'https': proxies[0],
# }
# print (req_proxies)
# r = requests.get('https://avito.ru', proxies=req_proxies)
# soup = BeautifulSoup(r.text, 'html.parser')
# print(soup.title)
def get_proxies():
    os.chdir('..')
    with open('data/checked_proxies.txt', 'r', encoding='UTF-8') as f:
        proxies = f.readlines()
    return proxies

def check_if_avito(proxy):
    driver = create_chrome_driver_object(proxy=proxy)
    driver.get('https://www.avito.ru/moskva_i_mo/planshety_i_elektronnye_knigi/planshety-ASgBAgICAUSYAoZO?bt=1&f=ASgBAQICAUSYAoZOAUD0vA0UkNI0&q=ipad+2020+32+-air+-pro+-mini+-cellular+-lte+-sim&s=104&user=1')
    contents = driver.page_source
    soup = BeautifulSoup(contents, 'lxml')
    print (soup.title)
proxies = get_proxies()
for proxy in proxies:
    check_if_avito(proxy)