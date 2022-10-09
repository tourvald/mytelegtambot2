import random
import re
import time

from bs4 import BeautifulSoup
import pickle
from mylibs import get_bs4_content
from my_libs.libs_selenium import create_chrome_driver_object

def get_stop_list():
    """возвращает стоп лист из файла stop_list.txt"""
    with open('data/work_with_links/stop_list.txt', 'r') as f:
        stop_list = f.readlines()
        return stop_list

def check_text_for_stop_words(stop_list, text):
    """проверяет содержит ли текст слово из стоп листа"""
    for stop_word in stop_list:
        if stop_word.lower().strip() in text.lower():
            return True
        else:
            return False

def generate_yesterdays_links():
    links_quanity = count_links_quanity('links.txt')
    for link_number in range(links_quanity):
        stop_search = make_awesome_link_list(link_number)
        if stop_search == True:
            break
        time.sleep(10)

def filter_links_by_content(file_with_links):
    links_quanity = count_links_quanity('data/work_with_links/item_links.txt')
    url = get_link(5,'data/work_with_links/item_links.txt')
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

def add_links_to_db(url):
    generate_pagination_links(url)
    generate_yesterdays_links()

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

def count_links_quanity(path_to_file):
    with open (path_to_file, 'r') as f:
        links = f.readlines()
    return int(len(links))

def get_link(link_number, path_to_file):
    with open (path_to_file, 'r') as f:
        link = f.readlines()[link_number]
    return link





# ДОБАВЛЕНИЕ НОВЫХ ССЫЛОК С ОБЪЯВЛЕНИЯМИ ПО ОБМЕНУ

def delete_bad_items(div_with_items):
    try:
        items_to_del = div_with_items.find_all('div', class_="items-vip-KXPvy")
        print(len(div_with_items))
        for item_to_del in items_to_del:
            item_to_del.clear()
        items_to_del = div_with_items.find_all('div', class_="items-witcher-VlS6v")
        for item_to_del in items_to_del:
            item_to_del.clear()
        print('Ненужные блоки удалены')
        print(len(div_with_items))
    except Exception as e:
        print('Ненужные блоки не найдены')

def make_awesome_link_list(soup):
    """Принимает СУП ссылки на поиск
    Добавляет в файл item_links.txt ссылки на объявления с обменами"""
    stop_search = False
    div_with_items = soup.find('div', class_='items-items-kAJAg')
    # print(len(div_with_items))
    # delete_bad_items(div_with_items)
    # print(len(div_with_items))
    # time.sleep(10)

    try:
        items_to_del = div_with_items.find_all('div', class_="items-vip-KXPvy")
        print(items_to_del)
        print(len(div_with_items))
        for item_to_del in items_to_del:
            item_to_del.clear()
        items_to_del = div_with_items.find_all('div', class_="items-witcher-VlS6v")
        print(items_to_del)
        for item_to_del in items_to_del:
            item_to_del.clear()
        print(len(div_with_items))
        div_with_items = soup.find('div', class_='items-items-kAJAg')
        print(len(div_with_items))
        time.sleep(10)
    except Exception as e:
        print(e)
    try:
        logged_in = soup.find('div', class_='index-services-menu-item_username-_YDXo')
        print(logged_in.text)
    except:
        print('Нет авторизации')

    items = div_with_items.find_all('div', {'data-marker':'item'})
    stop_words_counter = 0
    bad_rating_counter = 0
    for item in items:
        continue_ = 0
        items_tuple = {}
        items_tuple['url'] = 'https://www.avito.ru'+item.find('a').get('href')
        feedback = item.find('span', {'data-marker': "seller-rating/summary"})

        if feedback:
            feedback = feedback.text.split()[0]
            if int(feedback) > 20:
                continue_ = 1

        if item.find('div', class_="iva-item-descriptionStep-C0ty1"):
            items_tuple['description'] = item.find('div', class_="iva-item-descriptionStep-C0ty1").text
            print (items_tuple['description'])
            stop_list = get_stop_list()
            for stop_word in stop_list:
                if stop_word.lower().strip().replace('\n', '') in items_tuple['description'].lower().replace('/n', ''):
                    print ('Заблокировано по стоп слову', stop_word.lower().strip().replace("\n", ""))
                    stop_words_counter += 1
                    continue_ = 1
                    break
        else:
            items_tuple['description'] = 'Не удалось выгрузить описание'
            print (items_tuple['description'])
            print (items_tuple['url'])

        if continue_== 1:
            continue

        item_date = item.find('div', {'data-marker':'item-date'})
        if '1 день назад' not in item_date.text:
            continue_ = 1
        if '2 дня назад' in item_date.text:
            print('ОСТАНОВКА')
            stop_search = True
            break

        if continue_== 1:
            continue

        if item.find('span', class_='desktop-1lslbsi'):
            items_tuple['seller_rating'] = item.find('span', class_='desktop-1lslbsi').text
            items_tuple['seller_rating'] = float(items_tuple['seller_rating'].replace(',','.'))
            if  items_tuple['seller_rating'] < 3.6:
                bad_rating_counter +=1
                continue_ = 1
            else:
                print(items_tuple['seller_rating'])
        else:
            print(item.find('span', class_='desktop-1lslbsi'))

        if continue_== 1:
            continue

        items_tuple['title'] = item.find('a').get('title')
        print (items_tuple['url'])
        print(item_date.text)
        with open('data/work_with_links/item_links.txt', 'a') as f:
            f.write(items_tuple['url'] + '\n')
    print (f'Заблокировано по стоп - словам - {stop_words_counter} объявлений')
    print(f'Заблокировано из - зарейтинга - {bad_rating_counter} объявлений')
    return stop_search #


def get_links_to_parce(soup):
    """Принимает СУП поискового запроса авито
    возвращает ссылки на страницы поскового запроса, с которых нужно парсить объявления"""
    items_extraImage = soup.find('div', class_=re.compile('items-extraImage'))
    if items_extraImage:
        pages = 1
    else:
        pages = soup.find("div", {"data-marker": "pagination-button"}).find_all('span')[-2].text
    pagination_pages = soup.find('div', class_='pagination-pages')
    url = 'https://www.avito.ru'+pagination_pages.find_all('a', class_='pagination-page')[1].get('href')
    urls = []
    if '=2&q=' not in url:
        print('Сссылка не подходит!')
    urls.append(url.replace(f'=2&q=', f'=1&q='))
    urls.append(url)
    for page in range(2, int(pages)):
        urls.append(url.replace(f'=2&q=', f'={page + 1}&q='))
    return urls


def get_new_items_lite(url):
    print(f'В ОБРАБОТКЕ {url}')
    i1 = 0
    with open('data/checked_proxies.txt', 'r', encoding='UTF-8') as f:
        proxies = f.readlines()
    print(proxies)
    proxies.reverse()
    driver = create_chrome_driver_object( headless=True)
    driver.get(url)
    driver.implicitly_wait(10)
    try:
        for cookie in pickle.load(open('cookies/test_cookies.pkl', "rb")):
            driver.add_cookie(cookie)
        time.sleep(random.uniform(1,3))
        driver.refresh()
    except Exception as e:
        print ('Не удалось загрузить куки')

    for i in range(10):
        try:
            contents = driver.page_source
            soup = BeautifulSoup(contents, 'lxml')
            pages = get_links_to_parce(soup)
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
                make_awesome_link_list(soup)
                break
            except Exception as e:
                driver.refresh()
                print(f'Ждем {10+i1*3} сек')
                time.sleep(10+i1*3)
                print(e)

    # with open('test_cookies.pkl', 'wb') as f:
    #    f.close()
    # pickle.dump(driver.get_cookies(), open('cookies/test_cookies.pkl', 'wb'))

    driver.close()
    driver.quit()

# url = 'https://www.avito.ru/moskva/telefony/mobile-ASgBAgICAUSwwQ2I_Dc?f=ASgBAQECAUSwwQ2I_DcBQOjrDjT~_dsC_P3bAvr92wIBRcaaDBh7ImZyb20iOjgwMDAsInRvIjo1MDAwMH0&q=обмен&s=104&user=1'
# get_new_items_lite(url)






