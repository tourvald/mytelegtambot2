

from my_libs.libs_selenium import create_chrome_driver_object
import pandas as pd
from mylibs import get_bs4_from_driver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from time import sleep
import csv
from datetime import datetime, timedelta
from my_libs.cian.parce_cian import cian_parce_2
import os
import platform
# Определяем в какой системе мы находимся и задаем параметр для спуска в корневую дирректорию
print (platform.processor())
if platform.processor() == 'Intel64 Family 6 Model 42 Stepping 7, GenuineIntel':
	chdir_path = '../..'
else:
	chdir_path = '..'

def cian_get_links_from_report():
    # df = pd.read_csv(f'offers.xlsx', encoding='utf-8', delimiter=';')
    df = pd.read_excel('my_libs/cian/offers.xlsx', sheet_name='ЦИАН - Продажа городской')
    links_list = df['Ссылка на объявление'].tolist()
    # print(df.head())
    return (links_list)
def parce_many_links(link_list):
    df = pd.read_excel('my_libs/cian/bad_links.xlsx', engine='openpyxl')
    black_list = df['link'].tolist()
    print(black_list)

    good_links_list = []
    skipped_links = []
    bad_links_list = []
    df_bad_links = pd.DataFrame(columns=['link'])
    print(df_bad_links.head())
    print(f'(Количество ссылок - {len(link_list)} )')
    ii = 1
    for i in link_list:
        if i in black_list:
            print('ССЫЛКА В ЧЕРНОМ СПИСЬКЕ')
            continue
        ii = ii+1
        print(f'ПЫТАЕМСЯ СПАРСИТЬ {i}')
        try:
            average_flat_price, average_flat_price_nearby, flat_price = cian_parce_2(i)
            if (flat_price+50)/average_flat_price_nearby < 1.1 and (flat_price+50)/average_flat_price < 1.1:
                print (f'{average_flat_price}({round((flat_price+50)/average_flat_price, 2)}) - средняя цена по дому')
                print (f'{average_flat_price_nearby}({round((flat_price+50)/average_flat_price_nearby, 2)}) - средняя цена в округе')
                print (f'{round( ((flat_price+50)/average_flat_price_nearby + (flat_price+50)/average_flat_price)/2,2)} - общая оценка')
                print('Ссылка добавлена')
                outputs = []
                outputs.append(f'{flat_price} - Цена квартиры')
                outputs.append(f'{average_flat_price}({round((flat_price + 50) / average_flat_price, 2)}) - средняя цена по дому')
                outputs.append(f'{average_flat_price_nearby}({round((flat_price + 50) / average_flat_price_nearby, 2)}) - средняя цена в округе')
                outputs.append(f'{round(((flat_price + 50) / average_flat_price_nearby + (flat_price + 50) / average_flat_price) / 2, 2)} - общая оценка')
                good_links_list.append([i, outputs])
                print(good_links_list)
            else:
                print(f'{i} ДОБАВЛЕНА В ЧЕРНЫЙ СПИСОК')
                bad_links_list.append(i)
        except Exception as e:
            skipped_links.append(i)
            print(e)
        # if ii == 10:
        #     break
    print(bad_links_list)
    print(black_list)
    bad_links_list = bad_links_list + black_list
    print(bad_links_list)


    df_bad_links = pd.DataFrame(bad_links_list, columns=['link'])
    print(df_bad_links.head(100))
    df_bad_links.to_excel(f'my_libs/cian/bad_links.xlsx', engine='openpyxl', index=False)



    print('След ссылка')
    return (good_links_list)

def get_link_list_from_url(url='https://www.cian.ru/cat.php?currency=2&deal_type=sale&demolished_in_moscow_programm=0&engine_version=2&floornl=1&foot_min=11&is_first_floor=0&maxprice=15000000&minfloorn=6&minlift=1&minprice=9500000&mintarea=38&object_type%5B0%5D=1&offer_type=flat&only_flat=1&only_foot=2&outdated_repair=1&region=1&room1=1&room2=1&room9=1&sort=creation_date_desc&sost_type%5B0%5D=1&saved_search_id=38795982'):
    driver = create_chrome_driver_object(headless=False)
    driver.set_window_size(1366,768)
    driver.get(url)
    driver.implicitly_wait(10)
    sleep(4)
    link_list = []

    for i in range(1,100):
        el_with_items = driver.find_elements(By.CLASS_NAME, '_93444fe79c--media--9P6wN')
        for el in el_with_items:
            link_list.append(el.get_attribute('href'))
        try:
            next_btn = driver.find_elements(By.XPATH, '//*[@id="frontend-serp"]/div/div[5]/div[1]/nav/a/span')
            if len(next_btn) == 0:
                break
            for btn in next_btn:
                if btn.text == 'Дальше':
                    btn.click()
                    sleep(5)
        except Exception as e:
            print(e)
            break
    print(f'Найдено {len(link_list)} ссылок')
    print(link_list)
    return link_list



if __name__ == "__main__":
    os.chdir('../..')
    # print(os.getcwd())
    # links_list = cian_get_links_from_report()
    # print (parce_many_links(links_list))
    get_link_list_from_url()