

from my_libs.libs_selenium import create_chrome_driver_object
import pandas as pd
from mylibs import get_bs4_from_driver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from time import sleep
import csv
from datetime import datetime, timedelta
from parce_cian import cian_parce
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
    df = pd.read_excel('offers.xlsx', sheet_name='ЦИАН - Продажа городской')
    links_list = df['Ссылка на объявление'].tolist()
    # print(df.head())
    return (links_list)
def parce_many_links(link_list):
    good_links_list = []
    print(f'(Количество ссылок - {len(link_list)} )')
    for i in link_list:
        print(i)
        try:
            average_flat_price, average_flat_price_nearby, flat_price = cian_parce(i)
        except Exception as e:
            print('Не удалось спарсить страницу')
        if (flat_price+50)/average_flat_price_nearby < 1.1 and (flat_price+50)/average_flat_price < 1.1:
            try:
                print (f'{average_flat_price}({round((flat_price+50)/average_flat_price, 2)}) - средняя цена по дому')
                print (f'{average_flat_price_nearby}({round((flat_price+50)/average_flat_price_nearby, 2)}) - средняя цена в округе')
                print (f'{round( ((flat_price+50)/average_flat_price_nearby + (flat_price+50)/average_flat_price)/2,2)} - общая оценка')
                print('Ссылка добавлена')
                good_links_list.append(i)
            except Exception as e:
                print('Не удалось спарсить страницу')
        print('След ссылка')
    return (good_links_list)


if __name__ == "__main__":
    # os.chdir(chdir_path)
    links_list = cian_get_links_from_report()
    print (parce_many_links(links_list))