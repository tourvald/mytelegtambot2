import re
import numpy as np
import  pickle
from bs4 import BeautifulSoup
import time
import lxml
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
def av_price_sdt(price_list):
    print(f'START{price_list}')
    price_list = sorted(int(i) for i in price_list if re.fullmatch(r'\d+', i))
    print(f'SORTED{price_list}')
    price_list = price_list[int(len(price_list) * 0.1):len(price_list) - int(len(price_list) * 0.1)]
    price_list_std = int(np.std(price_list))
    price_list_to_remove_right = len(price_list) - 1
    price_list_to_remove_left = 0
    print (f'std = {price_list_std}')
    for i in range(len(price_list) // 2, 0, -1):
        if price_list[i] - price_list[i - 1] > price_list_std:
            price_list_to_remove_left = i
            print(price_list_to_remove_left)
            break

    for i in range(len(price_list) // 2, len(price_list), 1):
        if price_list[i] - price_list[i - 1] > price_list_std:
            price_list_to_remove_right = i - 1
            print(price_list_to_remove_right)
            break
    if len(price_list) > 5:
        if len(price_list[price_list_to_remove_left:price_list_to_remove_right]) > 2:
            price_list = price_list[price_list_to_remove_left:price_list_to_remove_right]
    print(f'FINAL{price_list}')

    av_price = int(np.average(price_list))
    print(f'Средняя цена = {av_price}')
    return av_price

def av_price_auto(price_list):
    print(f'START{price_list}')
    price_list = sorted(int(i) for i in price_list if re.fullmatch(r'\d+', i))
    print(f'SORTED{len(price_list),price_list}')
    #price_list = price_list[len(price_list)//10:(len(price_list)-len(price_list)//10)]
    price_list = price_list[4:44]
    print(f'SLICED{len(price_list),price_list}')
    av_price = int(np.average(price_list))
    print(f'Средняя цена = {av_price}')
    return av_price


def av_price_old(price_list):
    [price_list.remove(i) for i in price_list.copy() if i == "..."]  # Удаляем из списка значения без цен
    price_list = sorted([int(i) for i in price_list.copy()])  # Конвертируем список в integer

    new_price_list = price_list.copy()
    len_new_pice_list = len(new_price_list)
    print(f'Длинна списка - {len_new_pice_list};', end=' ')
    if len_new_pice_list > 11:
        new_price_list = new_price_list[len_new_pice_list // 5:len_new_pice_list - len_new_pice_list // 5]
        len_new_pice_list = len(new_price_list)

    std_new_price_list = np.std(new_price_list)

    for i in range(len_new_pice_list // 2, -1, -1):
        if new_price_list[i] - new_price_list[i - 1] > std_new_price_list:
            del new_price_list[0:i]
            break
    try:
        for i in range((len_new_pice_list // 2), len_new_pice_list, 1):
            if new_price_list[i] - new_price_list[i - 1] > std_new_price_list:
                del new_price_list[i:len_new_pice_list]
                break
    except Exception as e:
        print (f'{e}, avito_parcer_script.py, line 59')
        print (len(new_price_list))

    if len(price_list) > 11:
        price_list = price_list[
                     len(price_list) // 5:len(price_list) - len(price_list) // 5]  # Удаляем с конца и начала по 20%
    for i in range(len(price_list) // 2, -1, -1):
        if price_list[i] / price_list[i - 1] > 1.16:
            del price_list[0:i]
            break

    for i in range(len(price_list) // 2, len(price_list), 1):
        if price_list[i] / price_list[i - 1] > 1.08:
            del price_list[i:len(price_list)]
            break

    av_price = str(sum(price_list) // len(price_list))
    print(f'Средняя цена = {av_price}')
    return av_price

def get_bs4_content(url, headless=True, path_to_webdriver='settings/webdriver.txt', path_to_cookies='cookies.pkl'):
    with open(path_to_webdriver, 'r', encoding='utf-8') as f:
        web_driver = f.readline()
        f.close()  # Закрываем файл
    chromeOptions = selenium.webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chromeOptions.page_load_strategy = 'eager'
    chromeOptions.add_experimental_option("prefs", prefs)
    print (headless)
    if headless ==  True:
        print(f'headless={headless}')
        chromeOptions.add_argument('headless')
    chromeOptions.add_argument("--disable-blink-features=AutomationControlled")
    chromeOptions.add_argument("--ignore-ssl-errors")
    chromeOptions.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
    chromeOptions.add_argument("--disable-blink-features=AutomationControlled")  # Картинок
    chromeOptions.add_argument(
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 YaBrowser/21.3.3.230 Yowser/2.5 Safari/537.36")
    s = Service(executable_path=web_driver)
    driver = webdriver.Chrome(service=s, options=chromeOptions)
    print('Селениум успешно загружен')
    driver.get(url)
    time.sleep(6)
    for cookie in pickle.load(open('cookies/test_cookies.pkl', "rb")):
        driver.add_cookie(cookie)
    time.sleep(3)
    print('Куки загружены')
    driver.refresh()
    time.sleep(5)
    driver.refresh()
    print ('Ссылка успешно загружена')
    contents = driver.page_source
    soup = BeautifulSoup(contents, 'lxml')
    pickle.dump(driver.get_cookies(), open('cookies/avito.pkl', "wb"))
    driver.close()
    driver.quit()
    return soup

def create_chrome_driver_object(path_to_webdriver='settings/webdriver.txt', headless=False):
    with open(path_to_webdriver, 'r', encoding='utf-8') as f:
        web_driver = f.readline()
    chromeOptions = selenium.webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chromeOptions.page_load_strategy = 'eager'
    chromeOptions.add_experimental_option("prefs", prefs)
    if headless ==  True:
        print(f'headless={headless}')
        chromeOptions.add_argument('headless')
    chromeOptions.add_argument("--disable-blink-features=AutomationControlled")
    chromeOptions.add_argument("--ignore-ssl-errors")
    chromeOptions.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
    chromeOptions.add_argument("--disable-blink-features=AutomationControlled")  # Картинок
    chromeOptions.add_argument(
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 YaBrowser/21.3.3.230 Yowser/2.5 Safari/537.36")
    s = Service(executable_path=web_driver)
    driver = webdriver.Chrome(service=s, options=chromeOptions)
    return driver

def get_bs4_from_driver(driver, url='https://vk.com', cookies=False):
    driver.get(url)
    if cookies:
        for cookie in cookies:
            driver.add_cookie(cookie)
            time.sleep(2)
        driver.refresh()
        time.sleep(3)
    time.sleep(2)
    contents = driver.page_source
    soup = BeautifulSoup(contents, 'lxml')
    return soup



# url = 'https://www.avito.ru/moskva/telefony/mobile-ASgBAgICAUSwwQ2I_Dc?f=ASgBAQECAUSwwQ2I_DcBQOjrDjT~_dsC_P3bAvr92wIBRcaaDBh7ImZyb20iOjgwMDAsInRvIjo1MDAwMH0&q=обмен&s=104&user=1'
#
# driver = create_chrome_driver_object()
# driver.get('http://vk.com')
# driver.switch_to.new_window()
# driver.get('http://youla.ru')
# driver.switch_to.new_window()
# driver.get('https://avito.ru')
# time.sleep (3)
# for cookie in pickle.load(open('cookies/test_cookies.pkl', "rb")):
#     driver.add_cookie(cookie)
# driver.refresh()
# time.sleep(4)
# driver.switch_to.new_window()
# driver.get('https://avito.ru')
# driver.switch_to.window(driver.window_handles[0])
# time.sleep(2)
# driver.close()
# driver.switch_to.window(driver.window_handles[0])
# driver.close()
# driver.switch_to.window(driver.window_handles[0])
# driver.close()
# driver.switch_to.window(driver.window_handles[0])
# driver.close()
#
# time.sleep(10)
# driver.close()
# driver.quit()
# url = 'https://www.avito.ru/'
# # url = 'https://www.avito.ru/moskva_i_mo/telefony/mobilnye_telefony/apple-ASgBAgICAkS0wA3OqzmwwQ2I_Dc?bt=1&f=ASgBAQICAkS0wA3OqzmwwQ2I_DcBQOjrDjT~_dsC_P3bAvr92wI&q=%D0%BE%D0%B1%D0%BC%D0%B5%D0%BD+-%22%D0%BD%D0%B5+%D0%B8%D0%BD%D1%82%D0%B5%D1%80%D0%B5%D1%81%D0%B5%D0%BD%22+-%22%D0%BD%D0%B5+%D0%BF%D1%80%D0%B5%D0%B4%D0%BB%D0%B0%D0%B3%D0%B0%D1%82%D1%8C%22+-%22%D0%BD%D0%B5+%D0%B8%D0%BD%D1%82%D0%B5%D1%80%D0%B5%D1%81%D0%B5%D0%BD%22&s=104&user=1'
# get_bs4_content(url, headless=False)
# get_bs4_content('http://vk.com')