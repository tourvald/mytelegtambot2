from my_libs.libs_selenium import create_chrome_driver_object
from bs4 import BeautifulSoup
import time
import random
from multiprocessing import Pool
import json
from my_libs.libs_selenium import get_last_checked_proxy_number
def get_links_from_file(path_to_file):
    with open(path_to_file, 'r', encoding='UTF-8') as f:
        links = f.readlines()
    return links

links = get_links_from_file('data/neuro_learn/yes_links.txt')
# links = links[:7]
with open ('data/checked_proxies.txt', 'r', encoding='UTF-8') as f:
    proxies = f.readlines()
# proxies.append('None')
proxies.reverse()
len_proxies = len(proxies)
proxy_cycle = 0
count_proxies = 0
# count_proxies = get_last_checked_proxy_number()
driver = create_chrome_driver_object(proxy=proxies[count_proxies])



for link in links:
    loaded_ = None
    proxy_cycle = 0
    retryes = 0
    while proxy_cycle != 3:
        retryes += 1
        try:
            driver.get(link)
        except Exception as e:
            print (e.__cause__)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        if not soup.title:
            delay = random.uniform(2, 4)
            print(f'Cуп не получен, попытка {retryes}, ждем  {delay*retryes} сек')
            time.sleep(delay*retryes)
            if retryes == 7:
                retryes = 0
                driver.close()
                count_proxies += 1
                if count_proxies > len_proxies:
                    count_proxies = 0
                    proxy_cycle += 1
                    print(f'Загрузка не удалась. Попыток - {retryes}')
                driver = create_chrome_driver_object(proxy=proxies[count_proxies])
            continue
        try:
            title = soup.find('span', {'class' : 'closed-warning-content-2ooy4'})
            print (title.text)
            break
        except:
            print ('')

        if soup.title.text == 'Доступ временно заблокирован':
            print(soup.title.text)
            driver.close()
            count_proxies += 1
            if count_proxies > len_proxies:
                count_proxies = 0
                proxy_cycle += 1
                print(f'Загрузка не удалась. Попыток - {retryes}')
            driver = create_chrome_driver_object(proxy=proxies[count_proxies])
            continue

        h1 = company = soup.find('h1', {'class' : 'style-title-info-title-30L2Z'})
        description = soup.find('div', {'itemprop' : 'description'})

        try:
            print (h1.text, description.text)
            break
        except:
            print(soup.title)
            break

    delay = random.uniform(3, 6)
    time.sleep(delay)


last_proxy = proxies[count_proxies]
proxies.pop(count_proxies)
proxies.reverse()
proxies.append(last_proxy)
with open('data/checked_proxies.txt', 'w', encoding='UTF-8') as f:
    f.writelines(proxies)




# with open('data/neuro_learn/no_links_text.txt', 'a', encoding='UTF-8') as f:
#     f.writelines(f'{str(soup.title.text)}\n')
