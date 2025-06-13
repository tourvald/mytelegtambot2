import json
import os
from dotenv import load_dotenv
from multiprocessing import Pool
import chromedriver_autoinstaller
from selenium.webdriver.chrome.options import Options
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


def create_chrome_driver_object(headless=True, proxy=False):
    chromedriver_autoinstaller.install()  # Это загрузит и установит подходящий chromedriver

    chrome_options = Options()
    chrome_options.page_load_strategy = 'eager'
    if headless:
        print(f'headless={headless}', end=', ')
        chrome_options.add_argument('headless')
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--ignore-ssl-errors")
    chrome_options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
    chrome_options.add_argument(
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=chrome_options)
    return driver

if __name__ == '__main__':
    print("Начало теста")


