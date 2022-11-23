#coding: utf8
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

def get_link(link_number, path_to_file):
    with open (path_to_file, 'r') as f:
        link = f.readlines()[link_number]
    return link


# ДОБАВЛЕНИЕ НОВЫХ ССЫЛОК С ОБЪЯВЛЕНИЯМИ ПО ОБМЕНУ

def make_awesome_link_list(soup):
    """Принимает СУП ссылки на поиск
    Добавляет в файл item_links.txt ссылки на объявления с обменами"""
    stop_search = False
    div_with_items = soup.find('div', class_='items-items-kAJAg')

    try:
        items_to_del = div_with_items.find_all('div', class_="items-vip-KXPvy")
        for item_to_del in items_to_del:
            item_to_del.clear()
        items_to_del = div_with_items.find_all('div', class_="items-witcher-VlS6v")
        for item_to_del in items_to_del:
            item_to_del.clear()
        div_with_items = soup.find('div', class_='items-items-kAJAg')
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
        # werwer = input()
        continue_ = 0
        items_tuple = {}
        items_tuple['url'] = 'https://www.avito.ru'+item.find('a').get('href')
        feedback = item.find('span', {'data-marker': "seller-rating/summary"})

        if feedback:
            feedback = feedback.text.split()[0]
            if int(feedback) > 20:
                continue_ = 1

        item_name = item.find('h3', itemprop ="name").text
        # print(f'item_name = {item_name.text}')

        if item.find('div', class_="iva-item-descriptionStep-C0ty1"):
            items_tuple['description'] = item.find('div', class_="iva-item-descriptionStep-C0ty1").text.replace('/n', ' ')
            # print (items_tuple['description'])
            stop_list = get_stop_list()
            print(item_name)
            for stop_word in stop_list:
                if stop_word.lower().strip() in item_name.lower().strip():
                    print ('Заблокировано по стоп слову', stop_word.lower().strip().replace("\n", ""))
                    stop_words_counter += 1
                    continue_ = 1
                    break
                elif stop_word.lower().strip().replace('\n', '') in items_tuple['description'].lower().replace('/n', ''):
                    continue_ = 1
                    break

        if continue_== 1:
            continue
        # else:
        #     items_tuple['description'] = 'Не удалось выгрузить описание'
            # print (items_tuple['description'])
            # print (items_tuple['url'])
        # print(items_tuple['description'])
        if 'обмен' in item_name:
            print ('поиск обмена в названии - ', item_name)
            white_word_string = item_name
            print (white_word_string)
        elif 'обмен' in items_tuple['description']:
            white_word_position = int(items_tuple['description'].find('обмен'))
            # print ('поиск обмена в строке - ', white_word_position)
            # start = [white_word_position - 8 if white_word_position > 8 else 1]
            if white_word_position > 11:
                start = white_word_position - 12
            else:
                start = 0
            print('Старт - ', start)
            stop = white_word_position + 16

            print('Стоп - ', stop)
            white_word_string = items_tuple['description'][start:stop]
            #[white_word_position - 10: white_word_position + 16]
            print ('отрывок - ', white_word_string)
        else:
            print("Пропускаем, поскольку нет ключевого слова обмен")
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
            # input('Введите что-нибудь')
            continue

        items_tuple['title'] = item.find('a').get('title')
        # print (items_tuple['url'])
        # print(item_date.text)
        string_to_add = item_name + ' ' + white_word_string.strip().replace('\n',' ') + ' ' + items_tuple['url']
        print ('Записываем' + string_to_add)
        with open('data/work_with_links/item_links.txt', 'a' ,encoding='UTF-8') as f:
            f.write(string_to_add.strip()+'\n')
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

if __name__ == '__main__':
    # with open('data/work_with_links/item_links.txt', 'w') as f:
    #     f.close()
    url = 'https://www.avito.ru/moskva/telefony/mobile-ASgBAgICAUSwwQ2I_Dc?f=ASgBAQECAUSwwQ2I_DcBQOjrDjT~_dsC_P3bAvr92wIBRcaaDBh7ImZyb20iOjgwMDAsInRvIjo1MDAwMH0&q=обмен&s=104&user=1'
    # url = 'https://www.avito.ru/moskva/planshety_i_elektronnye_knigi?cd=1&f=ASgCAQICAUD0vA0UkNI0&q=обмен&s=104&user=1'
    get_new_items_lite(url)

    # stop_list = get_stop_list()
    # for word in stop_list:
    #     print (word.strip().encode())






