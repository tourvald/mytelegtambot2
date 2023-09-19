

from my_libs.libs_selenium import create_chrome_driver_object

from mylibs import get_bs4_from_driver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from time import sleep
import csv
from datetime import datetime, timedelta
import os
import platform
# Определяем в какой системе мы находимся и задаем параметр для спуска в корневую дирректорию
print (platform.processor())
if platform.processor() == 'Intel64 Family 6 Model 42 Stepping 7, GenuineIntel':
	chdir_path = '../..'
else:
	chdir_path = '..'

def cian_parce(url = "https://www.cian.ru/sale/flat/292602659/"):
    # ФОРМАТИРОВАНИЕ ФАЙЛА ЗАПИСИ ДАННЫХ
    filename = datetime.today().date()
    print (datetime.today().date())
    print (os.getcwd())

    driver = create_chrome_driver_object(headless=False)
    driver.maximize_window()

    # url = 'https://www.avito.ru/user/3927f5d35ba5d4e69a7ad7a45bed0cbf/profile/all/kvartiry?gdlkerfdnwq=101&shopId=3096698&page_from=from_item_card&iid=2972689148&sellerId=3927f5d35ba5d4e69a7ad7a45bed0cbf'
    driver.get(url)
    driver.implicitly_wait(10)
    sleep(4)

    # next_btn = driver.find_element(By.XPATH, '//*[@id="item_list_with_filters"]/div[2]/div/div[2]/div/div[2]/button[2]')

    flat_price_element = driver.find_element(By.CLASS_NAME, 'a10a3f92e9--item--iWTsg')
    flat_price = int(flat_price_element.text.split()[3])
    # print (f'Цена квартиры - {flat_price}')
    open_history_btn = driver.find_element(By.CLASS_NAME, 'a10a3f92e9--show-more-btn--wmYm5')
    #driver.execute_script("arguments[0].scrollIntoView(true);", open_history_btn)
    new_height = driver.execute_script("return document.body.scrollHeight")
    driver.execute_script(f"window.scrollTo({new_height}, -100)")
    sleep(5)
    # for i in range (1,11):
    #     driver.execute_script(f"window.scrollTo(0, {i*400})")
    #     sleep(3)

    # open_history_btn = driver.find_element(By.XPATH, '//*[@id="frontend-offer-card"]/div[2]/div[2]/div[7]/div[4]/div/div/div[3]/button')
    open_history_btn = driver.find_element(By.CLASS_NAME, 'a10a3f92e9--show-more-btn--wmYm5')
    sleep(2)
    open_history_btn.click()
    sleep(3)

    el_with_items = driver.find_element(By.CLASS_NAME, 'a10a3f92e9--inner--wbRIU')
    sleep(2)
    elements = el_with_items.text.split('\n')
    sum = 0
    el_count = 0
    for i in elements:
        if '₽/м²' in i:
            el = f'\n{i}'
            print(el.split()[0])
            sum = sum + int(el.split()[0])
            el_count = el_count + 1
    average_flat_price = int(sum/el_count)
        # else:
        #     print (i, end=' ')


    sleep(2)
    print('Завершен парсинг дома')
    flats_nearby = driver.find_elements(By.CLASS_NAME,'a10a3f92e9--button--LgLDi')

    for i in flats_nearby:
        if i.text == 'В соседних':
            break
    i.click()

    sleep(3)

    el_with_items = driver.find_element(By.CLASS_NAME, 'a10a3f92e9--inner--wbRIU')
    sleep(2)
    elements = el_with_items.text.split('\n')
    sum = 0
    el_count = 0
    for i in elements:
        if '₽/м²' in i:
            el = f'\n{i}'
            print(el.split()[0])
            sum = sum + int(el.split()[0])
            el_count = el_count + 1
    average_flat_price_nearby = int(sum/el_count)

    driver.close()
    driver.quit()
    return average_flat_price, average_flat_price_nearby, flat_price


def cian_parce_2(url = "https://www.cian.ru/sale/flat/292602659/"):
    # ФОРМАТИРОВАНИЕ ФАЙЛА ЗАПИСИ ДАННЫХ
    filename = datetime.today().date()
    print (datetime.today().date())
    print (os.getcwd())

    driver = create_chrome_driver_object(headless=False)
    driver.set_window_size(1366,768)

    # url = 'https://www.avito.ru/user/3927f5d35ba5d4e69a7ad7a45bed0cbf/profile/all/kvartiry?gdlkerfdnwq=101&shopId=3096698&page_from=from_item_card&iid=2972689148&sellerId=3927f5d35ba5d4e69a7ad7a45bed0cbf'
    driver.get(url)
    driver.implicitly_wait(10)
    sleep(4)

    # next_btn = driver.find_element(By.XPATH, '//*[@id="item_list_with_filters"]/div[2]/div/div[2]/div/div[2]/button[2]')

    flat_price_element = driver.find_element(By.CLASS_NAME, 'a10a3f92e9--item--iWTsg')
    flat_price = int(flat_price_element.text.split()[3])
    # print (f'Цена квартиры - {flat_price}')
    open_history_btn = driver.find_element(By.CLASS_NAME, 'a10a3f92e9--show-more-btn--wmYm5')
    #driver.execute_script("arguments[0].scrollIntoView(true);", open_history_btn)
    # new_height = driver.execute_script("return document.body.scrollHeight")
    # driver.execute_script(f"window.scrollTo({new_height}, -100)")
    # sleep(5)
    for i in range (1,25):
        driver.execute_script(f"window.scrollTo(500, {i*450})")
        sleep(0.35)
        try:
            open_history_btn = driver.find_element(By.CLASS_NAME, 'a10a3f92e9--show-more-btn--wmYm5')
            open_history_btn.click()
            break
        except Exception as e:
            continue


    # open_history_btn = driver.find_element(By.XPATH, '//*[@id="frontend-offer-card"]/div[2]/div[2]/div[7]/div[4]/div/div/div[3]/button')
    # open_history_btn = driver.find_element(By.CLASS_NAME, 'a10a3f92e9--show-more-btn--wmYm5')
    # sleep(2)
    # open_history_btn.click()

    el_with_items = driver.find_element(By.CLASS_NAME, 'a10a3f92e9--inner--wbRIU')
    elements = el_with_items.text.split('\n')
    sum = 0
    el_count = 0
    for i in elements:
        if '₽/м²' in i:
            el = f'\n{i}'
            print(el.split()[0])
            sum = sum + int(el.split()[0])
            el_count = el_count + 1
    average_flat_price = int(sum/el_count)
        # else:
        #     print (i, end=' ')


    sleep(2)
    print('Завершен парсинг дома')
    flats_nearby = driver.find_elements(By.CLASS_NAME,'a10a3f92e9--button--LgLDi')

    for i in flats_nearby:
        if i.text == 'В соседних':
            break
    i.click()

    sleep(2)

    el_with_items = driver.find_element(By.CLASS_NAME, 'a10a3f92e9--inner--wbRIU')
    elements = el_with_items.text.split('\n')
    sum = 0
    el_count = 0
    for i in elements:
        if '₽/м²' in i:
            el = f'\n{i}'
            print(el.split()[0])
            sum = sum + int(el.split()[0])
            el_count = el_count + 1
    average_flat_price_nearby = int(sum/el_count)

    driver.close()
    driver.quit()
    return average_flat_price, average_flat_price_nearby, flat_price

def download_db_exel():
    url = 'https://www.cian.ru/cat.php?currency=2&deal_type=sale&demolished_in_moscow_programm=0&engine_version=2&floornl=1&foot_min=11&is_first_floor=0&maxprice=15000000&minfloorn=6&minlift=1&minprice=9500000&mintarea=38&object_type%5B0%5D=1&offer_type=flat&only_flat=1&only_foot=2&outdated_repair=1&region=1&room1=1&room2=1&room9=1&sort=creation_date_desc&sost_type%5B0%5D=1&saved_search_id=38795982'
    url = 'https://www.cian.ru/cat.php?currency=2&deal_type=sale&demolished_in_moscow_programm=0&engine_version=2&floornl=1&foot_min=11&is_first_floor=0&maxprice=15000000&minfloorn=6&minlift=1&minprice=9500000&mintarea=38&object_type%5B0%5D=1&offer_type=flat&only_flat=1&only_foot=2&outdated_repair=1&region=1&room1=1&room2=1&room9=1&sort=creation_date_desc&sost_type%5B0%5D=1&saved_search_id=38795982#:~:text=%D0%A1%D0%BE%D1%85%D1%80%D0%B0%D0%BD%D0%B8%D1%82%D1%8C-,%D1%84%D0%B0%D0%B9%D0%BB,-Excel'
    filename = datetime.today().date()
    print (datetime.today().date())
    print (os.getcwd())
    driver = create_chrome_driver_object(headless=False)
    driver.set_window_size(1366,768)
    driver.get(url)
    driver.implicitly_wait(10)
    sleep(7)


if __name__ == "__main__":
    os.chdir(chdir_path)
    # download_db_exel()
    print(cian_parce_2('https://www.cian.ru/sale/flat/292629736/'))