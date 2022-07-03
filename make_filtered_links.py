import pickle
import random
from bs4 import BeautifulSoup
import time
from mylibs import get_bs4_content
from work_with_links import get_link, count_links_quanity, make_awesome_link_list
from write_links_to_file import get_quanity_pages
from my_libs.libs_selenium import create_chrome_driver_object
from work_with_links import make_awesome_link_list_2
import pickle
import random
import time

from bs4 import BeautifulSoup

from my_libs.libs_selenium import create_chrome_driver_object
from mylibs import get_bs4_content
from work_with_links import get_link, count_links_quanity, make_awesome_link_list
from work_with_links import make_awesome_link_list_2
from write_links_to_file import get_quanity_pages


def generate_pagination_links(url):
    soup = get_bs4_content(url, headless=True)
    pages = get_quanity_pages(soup)
    print (f'Страниц найдено - {len(pages)+1}')
    with open ('links.txt', 'w') as f:
        f.close()
    for page in pages:
        with open ('links.txt', 'a') as f:
            f.write(page+'\n')
        print (page)

def generate_pagination_links_2(soup):
    pages = get_quanity_pages(soup)
    print (f'Страниц найдено - {len(pages)+1}')
    for page in pages:
        print (page)
    return pages

def clear_file_with_item_links(path_to_file):
    with open (path_to_file, 'w') as f:
        f.close()

def generate_yesterdays_links():
    links_quanity = count_links_quanity('links.txt')
    for link_number in range(links_quanity):
        stop_search = make_awesome_link_list(link_number)
        if stop_search == True:
            break
        time.sleep(10)

def filter_links_by_content(file_with_links):
    links_quanity = count_links_quanity('item_links.txt')
    url = get_link(5,'item_links.txt')
    soup = get_bs4_content(url)
    item_owner_status = soup.find('div', class_='item-owner-status-root-3jRSs')
    item_owner_rating = soup.find('span', class_='style-seller-info-rating-score-KA-Kw')
    item_owner_info_value = soup.find_all('div', class_="style-seller-info-value-2YyZm")

    if item_owner_status:
        print (f'Онлайн статус найден- {item_owner_status.text}')
    else:
        print (f'Онлайн статус не найден - {item_owner_status}')

    if item_owner_rating:
        item_owner_rating = item_owner_rating.text.replace(',','.')
        if float(item_owner_rating) > 3.7:
            print (f'Рейтинг продавца подходит - {float(item_owner_rating)}')
        else:
            print (f'Рейтинг продавца НЕ подходит - {float(item_owner_rating)}')
    else:
        print (item_owner_rating)

    if item_owner_info_value[1]:
        print (item_owner_info_value[1].text.split(' ')[-1])
    else:
        print ('Вэлью нету нихуя')
    print(url)




# url = 'https://www.avito.ru/moskva/telefony/mobile-ASgBAgICAUSwwQ2I_Dc?f=ASgBAQECAUSwwQ2I_DcBQOjrDjT~_dsC_P3bAvr92wIBRcaaDBh7ImZyb20iOjgwMDAsInRvIjoyNTAwMH0&p=2&q=%D0%BE%D0%B1%D0%BC%D0%B5%D0%BD&s=104&user=1'
def add_links_to_db(url):
    generate_pagination_links(url)
    generate_yesterdays_links()

url = 'https://www.avito.ru/moskva/telefony/mobile-ASgBAgICAUSwwQ2I_Dc?f=ASgBAQECAUSwwQ2I_DcBQOjrDjT~_dsC_P3bAvr92wIBRcaaDBh7ImZyb20iOjgwMDAsInRvIjo1MDAwMH0&q=обмен&s=104&user=1'
def get_new_items(url):
    with open('data/checked_proxies.txt', 'r', encoding='UTF-8') as f:
        proxies = f.readlines()
    print(proxies)
    proxies.reverse()
    proxy_cycle = 0
    driver = create_chrome_driver_object(proxy=proxies[proxy_cycle])
    driver.get(url)
    try:
        for cookie in pickle.load(open('cookies/test_cookies.pkl', "rb")):
            driver.add_cookie(cookie)
        time.sleep(random.uniform(1,3))
        driver.refresh()
    except Exception as e:
        print (e)

    for i in range(5):
        try:
            contents = driver.page_source
            soup = BeautifulSoup(contents, 'lxml')
            pages = generate_pagination_links_2(soup)
            break
        except Exception as e:
            driver.refresh()
            print ('Ждем 5 сек')
            time.sleep(5)
            print (e)

    for i in range(1,len(pages)):
        time.sleep(random.uniform(1, 2))
        driver.get(pages[i])
        driver.switch_to.new_window()
        if i > 5:
            break
    time.sleep(random.uniform(1,5))
    for i in range(1,len(pages)):
        driver.switch_to.window(driver.window_handles[i - 1])
        for i1 in range(5):
            try:
                contents = driver.page_source
                soup = BeautifulSoup(contents, 'lxml')
                make_awesome_link_list_2(soup)
                break
            except Exception as e:
                driver.refresh()
                print ('Ждем 5 сек')
                time.sleep(5)
                print (e)
        if i > 4:
            break
    driver.close()
    driver.quit()

def get_new_items_lite(url):
    i1 = 0
    with open('data/checked_proxies.txt', 'r', encoding='UTF-8') as f:
        proxies = f.readlines()
    print(proxies)
    proxies.reverse()
    proxy_cycle = 0
    driver = create_chrome_driver_object(proxy=proxies[proxy_cycle])
    driver.get(url)
    driver.implicitly_wait(10)
    try:
        for cookie in pickle.load(open('cookies/test_cookies.pkl', "rb")):
            driver.add_cookie(cookie)
        time.sleep(random.uniform(1,3))
        driver.refresh()
    except Exception as e:
        print (e)

    for i in range(10):
        try:
            contents = driver.page_source
            soup = BeautifulSoup(contents, 'lxml')
            pages = generate_pagination_links_2(soup)
            break
        except Exception as e:
            driver.refresh()
            print(f'Ждем {10 + i1 * 3} сек')
            time.sleep(10 + i1 * 3)
            print (e)

    pages = pages[:3]

    for page in pages:
        driver.get(page)
        for i1 in range(10):
            try:
                contents = driver.page_source
                soup = BeautifulSoup(contents, 'lxml')
                make_awesome_link_list_2(soup)
                break
            except Exception as e:
                driver.refresh()
                print(f'Ждем {10+i1*3} сек')
                time.sleep(10+i1*3)
                print(e)

    with open('test_cookies.pkl', 'wb') as f:
       f.close()
    pickle.dump(driver.get_cookies(), open('cookies/test_cookies.pkl', 'wb'))

    driver.close()
    driver.quit()

# url = 'https://www.avito.ru/moskva/telefony/mobile-ASgBAgICAUSwwQ2I_Dc?f=ASgBAQECAUSwwQ2I_DcBQOjrDjT~_dsC_P3bAvr92wIBRcaaDBh7ImZyb20iOjgwMDAsInRvIjo1MDAwMH0&q=обмен&s=104&user=1'
# get_new_items_lite(url)





