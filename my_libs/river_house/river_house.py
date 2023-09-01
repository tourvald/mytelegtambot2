from my_libs.libs_selenium import create_chrome_driver_object
from mylibs import get_bs4_from_driver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from time import sleep
import csv
from datetime import datetime, timedelta
import os
def write_items_to_file(items):
    for i in items:
        item = i.text.split()

        item.pop(1)
        item.pop(2)
        item.pop(3)
        item = item[:7]
        item[3] = int(item[3]+item[4]+item[5])
        item = item[:8]

        if item[6] == '₽':
            #print('Проверка на рубль пройдена')
            pass
        else:
            print('Прокарка на Рубль НЕ ПРОЙДЕНА!!!!')
        item[2] = item[2][:-3]

        item = item[:4]
        item[0] = item[0][:1]
        item[0] = f'{item[0]}-{item[1]}-{item[2]}'
        # item[0].replace(',','!')
        item.pop(1)
        item.pop(1)
        print(item)

        with open(filepath, 'a', encoding='UTF-8') as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(item)
os.chdir('..')

# ФОРМАТИРОВАНИЕ ФАЙЛА ЗАПИСИ ДАННЫХ
filename = datetime.today().date()
print (datetime.today().date())
filepath = f'data/river_house/{filename}.csv'
with open(filepath, 'w', encoding='UTF-8') as f:
    writer = csv.writer(f, delimiter=";")
    head = ['id', datetime.today().date()]
    writer.writerow(head)

driver = create_chrome_driver_object(headless=False)
# url = "https://www.avito.ru/user/3927f5d35ba5d4e69a7ad7a45bed0cbf/profile?gdlkerfdnwq=101&shopId=3096698&page_from=from_item_card&iid=2972689148"
url = 'https://www.avito.ru/user/3927f5d35ba5d4e69a7ad7a45bed0cbf/profile/all/kvartiry?gdlkerfdnwq=101&shopId=3096698&page_from=from_item_card&iid=2972689148&sellerId=3927f5d35ba5d4e69a7ad7a45bed0cbf'
driver.get(url)
driver.implicitly_wait(10)
sleep(10)

# next_btn = driver.find_element(By.XPATH, '//*[@id="item_list_with_filters"]/div[2]/div/div[2]/div/div[2]/button[2]')
next_btn = driver.find_element(By.XPATH, '//*[@id="item_list_with_filters"]/div[2]/div/div[2]/div/nav/ul/li[9]/a')

items = driver.find_elements(By.CLASS_NAME, 'styles-responsive-m3Vnz')
write_items_to_file(items)
for i in range (1,20):
    try:
        next_btn.click()
        sleep(5)
    except WebDriverException:
        print ('Страницы закончились')
        break
    driver.implicitly_wait(10)
    items = driver.find_elements(By.CLASS_NAME, 'styles-responsive-m3Vnz')
    write_items_to_file(items)
