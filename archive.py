import json
def archive(search_date, search_link, av_price, search_request):

    with open('data/archive.json', 'r', encoding='utf-8') as f:
        file=f.read()
        f.close()
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
    if len(keys) == 1:
        date = list(arch[keys[0]].keys())[-1]
        link = arch[keys[0]][date]['link']
        return link
    else:
        return 'Запросов больше одного либо таких запросов не существует'

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


