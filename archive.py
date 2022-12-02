import datetime
import json
import random
import time


def archive(search_date, search_link, av_price, search_request):
    with open('data/archive.json', 'r', encoding='utf-8') as f:
        file=f.read()
    archive = json.loads(file)
    if str(archive.get(search_request)) == "None":
        print("Такого ключа нет")
        add_archive = {
        search_request: {
             str(search_date): {
                "price": av_price,
                "link": search_link
             }
         }
        }
        archive.update(add_archive)
    else:
        print("Такой ключ есть")
        archive[search_request].update({
            str(search_date): {
                "price": av_price,
                "link": search_link
                }
            })
    print ('архивируем', search_request)
    with open("data/archive.json", "w") as f:
        json.dump(archive, f, indent=1)
        f.close()

    # for item in archive[search_request]:
    #     print (archive[search_request][item])
    return()

def load_archive():
    with open('data/archive.json', 'r', encoding='utf-8') as f:
        arch = json.loads(f.read())
    return arch

def get_keys_list (req):
    arch = load_archive()
    keys = [key for key in arch.keys() if req in key]
    list(keys)
    return keys

def get_last_date(req):
    arch = load_archive()
    keys = get_keys_list(req)
    try:
        date = list(arch[keys[0]].keys())[-1]
        return date
    except:
        return 'Запросов больше одного либо таких запросов не существует'

def get_last_price(req):
    arch = load_archive()
    try:
        date = get_last_date(req)
        price = arch[req][date]['price']
        return (price)
    except:
        return 'Запросов больше одного либо таких запросов не существует'

def get_key_link (req):
    arch = load_archive()
    keys = [key for key in arch.keys() if req in key]
    if req in keys:
        date = list(arch[req].keys())[-1]
        link = arch[req][date]['link']
        return link
    else:
        return 'Не удалось найти ссылку по такому запросу'

def change_key_link (req, link):
    arch = load_archive()
    keys = [key for key in arch.keys() if req in key]
    if len(keys) == 1:
        date = list(arch[keys[0]].keys())[-1]
        price = arch[keys[0]][date]['price']
        arch[req].update({
            str(date): {
                "price": price,
                "link": link
                }
            })
        with open("data/archive.json", "w") as f:
            json.dump(arch, f, indent=4)
            f.close()
        return link
    else:
        return 'Запросов больше одного либо таких запросов не существует'

def delete_key (req):
    with open('data/archive.json', 'r', encoding='utf-8') as f:
        file=f.read()
    archive = json.loads(file)
    keys = get_keys_list(req)
    print(keys)
    print(len(archive))
    del archive[keys[0]]
    print(len(archive))
    with open("data/archive.json", "w") as f:
        json.dump(archive, f, indent=1)
        f.close()

def get_price_history(req:str) -> list:
    prices_history = []
    return_ = []
    previous_month = '0'
    archive = load_archive()
    keys = get_keys_list(req)
    dates = archive[keys[0]].keys()
    for date in dates:
        prices_history.append([date, archive[keys[0]][date]['price']])

    for price in prices_history:
        month = price[0].split('-')[1]
        if month != previous_month and month != '0':
            return_.append(price)
        previous_month = month
    return return_


def get_whole_price_history(req:str) -> list:
    prices_history = []
    return_ = []
    previous_month = '0'
    archive = load_archive()
    keys = get_keys_list(req)
    dates = archive[keys[0]].keys()
    for date in dates:
        return_.append([date, archive[keys[0]][date]['price']])

    return return_


def archive_status():
    amount = 0
    arch = load_archive()
    for key in arch:
        date = get_last_date(key)
        timedelta = (datetime.datetime.today() - datetime.datetime.strptime(date, '%Y-%m-%d')).days

        if  timedelta > 7:
            amount += 1
    return amount


if __name__ == '__main__':
    req = 'iphone 12 pro max 128'
    x = get_price_history(req)
    for y in x:
        print (y)

