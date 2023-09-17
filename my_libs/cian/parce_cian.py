

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
    sleep(5)

    # next_btn = driver.find_element(By.XPATH, '//*[@id="item_list_with_filters"]/div[2]/div/div[2]/div/div[2]/button[2]')

    flat_price_element = driver.find_element(By.CLASS_NAME, 'a10a3f92e9--item--iWTsg')
    flat_price = int(flat_price_element.text.split()[3])
    # print (f'Цена квартиры - {flat_price}')
    open_history_btn = driver.find_element(By.CLASS_NAME, 'a10a3f92e9--show-more-btn--wmYm5')
    driver.execute_script("arguments[0].scrollIntoView(true);", open_history_btn)
    sleep(2)
    new_height = driver.execute_script("return document.body.scrollHeight")
    driver.execute_script(f"window.scrollTo({new_height}, -200)")
    sleep(2)
    # for i in range (1,11):
    #     driver.execute_script(f"window.scrollTo(0, {i*500})")
    #     open_history_btn = driver.find_element(By.CLASS_NAME, 'a10a3f92e9--show-more-btn--wmYm5')
    #     driver.execute_script("arguments[0].scrollIntoView();", open_history_btn)
    #     print(open_history_btn.is_enabled())
    #     sleep(1)

    # open_history_btn = driver.find_element(By.XPATH, '//*[@id="frontend-offer-card"]/div[2]/div[2]/div[7]/div[4]/div/div/div[3]/button')
    open_history_btn = driver.find_element(By.CLASS_NAME, 'a10a3f92e9--show-more-btn--wmYm5')
    open_history_btn.click()
    sleep(3)

    el_with_items = driver.find_element(By.CLASS_NAME, 'a10a3f92e9--inner--wbRIU')
    elements = el_with_items.text.split('\n')
    sum = 0
    el_count = 0
    for i in elements:
        if '₽/м²' in i:
            el = f'\n{i}'
            # print(el.split()[0])
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
    elements = el_with_items.text.split('\n')
    sum = 0
    el_count = 0
    for i in elements:
        if '₽/м²' in i:
            el = f'\n{i}'
            # print(el.split()[0])
            sum = sum + int(el.split()[0])
            el_count = el_count + 1
    average_flat_price_nearby = int(sum/el_count)
        # else:
        #     print (i, end=' ')

    # items = el_with_items.find_element(By.CLASS_NAME, 'a10a3f92e9--item--dSgP3')
    # print (items)
    # items = driver.find_element(By.CLASS_NAME, 'a10a3f92e9--show-more-btn--wmYm5')
    # print(f'Найдено - {len(items)} эелементов с ценами')
    # write_items_to_file(items, filepath)
    # for i in range (1,20):
    #     try:
    #         next_btn.click()
    #         sleep(5)
    #     except WebDriverException:
    #         print ('Страницы закончились')
    #         break
    #     driver.implicitly_wait(10)
    #     items = driver.find_elements(By.CLASS_NAME, 'iva-item-body-KLUuy')
    #     print(f'Найдено - {len(items)} эелементов с ценами')
    #     write_items_to_file(items, filepath)
    driver.close()
    driver.quit()
    return average_flat_price, average_flat_price_nearby, flat_price
if __name__ == "__main__":
    os.chdir(chdir_path)
    print(cian_parce())