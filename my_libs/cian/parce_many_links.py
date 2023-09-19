

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
            pass
        ii = ii+1
        print(i)
        try:
            average_flat_price, average_flat_price_nearby, flat_price = cian_parce_2(i)
            if (flat_price+50)/average_flat_price_nearby < 1.1 and (flat_price+50)/average_flat_price < 1.1:
                print (f'{average_flat_price}({round((flat_price+50)/average_flat_price, 2)}) - средняя цена по дому')
                print (f'{average_flat_price_nearby}({round((flat_price+50)/average_flat_price_nearby, 2)}) - средняя цена в округе')
                print (f'{round( ((flat_price+50)/average_flat_price_nearby + (flat_price+50)/average_flat_price)/2,2)} - общая оценка')
                print('Ссылка добавлена')
                good_links_list.append([i,flat_price,average_flat_price,f'{average_flat_price}{round( ((flat_price+50)/average_flat_price))}',f'{average_flat_price_nearby}({round(((flat_price + 50) / average_flat_price_nearby))}'])

                print(good_links_list)
            else:
                bad_links_list.append(i)
        except Exception as e:
            print(e)
        if ii == 30:
            break
    print(bad_links_list)
    print(black_list)
    bad_links_list = bad_links_list + black_list
    print(bad_links_list)


    df_bad_links = pd.DataFrame(bad_links_list, columns=['link'])
    print(df_bad_links.head(100))
    df_bad_links.to_excel(f'my_libs/cian/bad_links.xlsx', engine='openpyxl', index=False)

    print('След ссылка')
    return (good_links_list)


if __name__ == "__main__":
    os.chdir('../..')
    print(os.getcwd())
    links_list = cian_get_links_from_report()
    print (parce_many_links(links_list))