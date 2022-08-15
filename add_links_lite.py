from make_filtered_links import get_new_items_lite
from multiprocessing import Pool

def work_with_links():

    '''добавляет новые ссылки с объявлениями по обменам за вчерашний день'''
    with open('item_links.txt', 'w', encoding='UTF-8') as f:
        f.close()
    with open('data/links_to_parce.txt', 'r', encoding='UTF-8') as f:
        urls = f.readlines()

    p = Pool(processes=1)
    p.map(get_new_items_lite, urls)

    with open('item_links.txt', 'r', encoding='UTF-8') as f:
        item_links = f.readlines()
    with open('old_links.txt', 'r', encoding='UTF-8') as f:
        old_links = f.readlines()
    links_to_add = set(item_links) - set(old_links)
    with open('old_links.txt', 'w', encoding='UTF-8') as f:
        f.writelines(item_links)
    with open('new_links.txt', 'a', encoding='UTF-8') as f:
        f.writelines(links_to_add)
    new_links_quanity = len(links_to_add)
    with open('new_links.txt', 'r', encoding='UTF-8') as f:
        string = f.readlines()
    msg = string[0]
    string.pop(0)
    with open('new_links.txt', 'w', encoding='UTF-8') as f:
        f.writelines(string)

    return new_links_quanity, msg