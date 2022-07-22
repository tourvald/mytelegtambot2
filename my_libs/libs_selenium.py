import json
import os
from dotenv import load_dotenv
from multiprocessing import Pool

import requests
import selenium
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from sys import platform


def get_last_checked_proxy_number():
    with open('settings/bot_settings.json', 'r', encoding='utf-8') as f:
        bot_settings = json.loads(f.read())
    return bot_settings['get_last_checked_proxy_number']

def create_chrome_driver_object(headless=True, proxy=None):
    load_dotenv()
    if platform == "darwin":
        path_to_webdriver = os.getenv("PATH_TO_WEBDRIVER_MAC")
    elif platform == "win32":
        path_to_webdriver = os.getenv("PATH_TO_WEBDRIVER_PC")
    chromeOptions = selenium.webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chromeOptions.page_load_strategy = 'eager'
    chromeOptions.add_experimental_option("prefs", prefs)
    if headless ==  True:
        print(f'headless={headless}', end=', ')
        chromeOptions.add_argument('headless')
    chromeOptions.add_argument("--disable-blink-features=AutomationControlled")
    chromeOptions.add_argument("--ignore-ssl-errors")
    chromeOptions.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
    chromeOptions.add_argument("--disable-blink-features=AutomationControlled")  # Картинок
    chromeOptions.add_argument(
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36")
    chromeOptions.add_experimental_option("excludeSwitches", ["enable-automation"])
    chromeOptions.add_experimental_option('useAutomationExtension', False)
    if 'NAA' not in proxy:
        if proxy:
            print(f'proxy={proxy}')
            chromeOptions.add_argument(f'--proxy-server={proxy}')
    s = Service(executable_path=path_to_webdriver)
    driver = webdriver.Chrome(service=s, options=chromeOptions)
    return driver

def check_proxy_list():
    working = 0
    os.chdir('..')
    print(os.getcwd())
    with open('data/proxies.txt', 'r', encoding='UTF-8') as f:
        proxies = f.readlines()
    with open('data/checked_proxies.txt', 'w', encoding='UTF-8') as f:
        f.close()
    for proxy in proxies:
        try:
            driver = create_chrome_driver_object(proxy=proxy)
            driver.get('https://httpbin.org/ip')
            contents = driver.page_source
            soup = (BeautifulSoup(contents, 'lxml'))
            print (soup.html)
            working +=1
            with open('data/checked_proxies.txt', 'a', encoding='UTF-8') as f:
                f.writelines(proxy)
        except Exception:
            pass
    print(f'Рабочик прокси - {working}')
    driver.close()

def get_proxyies():
    os.chdir('..')
    print(os.getcwd())
    with open('data/proxies.txt', 'r', encoding='UTF-8') as f:
        proxies = f.readlines()
    return proxies

def chek_proxy_requests(proxy):
    with open('data/checked_proxies.txt', 'w', encoding='UTF-8') as f:
        f.close()
    req_proxies = {
      'http': proxy,
      'https': proxy,
    }
    print(proxy)
    try:
        r = requests.get('https://www.avito.ru', proxies=req_proxies)
        print (req_proxies, proxy)
        return proxy
    except:
        pass

def check_proxy_list_requests():
    proxies = get_proxyies()
    p = Pool(processes=500)
    res = p.map(chek_proxy_requests, proxies)
    p.close()
    print(res)
    with open('data/checked_proxies.txt', 'w', encoding='UTF-8') as f:
        f.close()
    for i in res:
        if i:
            with open('data/checked_proxies.txt', 'a', encoding='UTF-8') as f:
                f.writelines(i)

if __name__ == '__main__':
    check_proxy_list_requests()


