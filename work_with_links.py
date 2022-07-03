import time
import pickle
from mylibs import get_bs4_content


def get_stop_list():
    """Получаем стоп лист из файла stop_list.txt"""
    with open('stop_list.txt', 'r') as f:
        stop_list = f.readlines()
        return stop_list

def count_links_quanity(path_to_file):
    with open (path_to_file, 'r') as f:
        links = f.readlines()
    return int(len(links))

def get_link(link_number, path_to_file):
    with open (path_to_file, 'r') as f:
        link = f.readlines()[link_number]
    return link

def check_text_for_stop_words(stop_list, text):
    for stop_word in stop_list:
        if stop_word in text:
            return True
        else:
            return False

def make_awesome_link_list(link_number):
    stop_search = False
    soup = get_bs4_content(get_link(link_number, 'links.txt'),headless=True)
    div_with_items = soup.find('div', class_='items-items-kAJAg')
    try:
        items_to_del = div_with_items.find_all('div', class_="items-vip-KXPvy")
        for item_to_del in items_to_del:
            item_to_del.clear()
        items_to_del = div_with_items.find_all('div', class_="items-witcher-VlS6v")
        for item_to_del in items_to_del:
            item_to_del.clear()
    except Exception as e:
        print (e)

def make_awesome_link_list_2(soup):
    stop_search = False
    div_with_items = soup.find('div', class_='items-items-kAJAg')
    try:
        items_to_del = div_with_items.find_all('div', class_="items-vip-KXPvy")
        for item_to_del in items_to_del:
            item_to_del.clear()
        items_to_del = div_with_items.find_all('div', class_="items-witcher-VlS6v")
        for item_to_del in items_to_del:
            item_to_del.clear()
    except Exception as e:
        print(e)


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
            stop_list = get_stop_list()
            for stop_word in stop_list:
                if stop_word.lower().strip() in items_tuple['description'].lower():
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
        # print (f'ПРИНЯТО - {items_tuple["title"]}')
        print (items_tuple['url'])

        print(item_date.text)
        with open('item_links.txt', 'a') as f:
            f.write(items_tuple['url'] + '\n')
    print (f'Заблокировано по стоп - словам - {stop_words_counter} объявлений')
    print(f'Заблокировано из - зарейтинга - {bad_rating_counter} объявлений')
    return stop_search


# with open ('item_links.txt', 'w') as f:
#     f.close()
# links_quanity = count_links_quanity('links.txt')
# for link_number in range(links_quanity):
#     stop_search = make_awesome_link_list(link_number)
#     if stop_search == True:
#         break
#     time.sleep(10)





