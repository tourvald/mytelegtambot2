import re
from mylibs import get_bs4_content

def get_quanity_pages (soup):
    items_extraImage = soup.find('div', class_=re.compile('items-extraImage'))
    if items_extraImage:
        pages = 1
    else:
        pages = soup.find("div", {"data-marker": "pagination-button"}).find_all('span')[-2].text
        # for i in soup.find("div", {"data-marker": "pagination-button"}).find('span', {'data-marker':'page(...)'}).find_next():
        #     print (i)
        # for i in soup.find("div", {"data-marker": "pagination-button"}).find_all('span'):
        #     print (i)


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



# url = 'https://www.avito.ru/moskva/telefony/mobile-ASgBAgICAUSwwQ2I_Dc?f=ASgBAQECAUSwwQ2I_DcBQOjrDjT~_dsC_P3bAvr92wIBRcaaDBh7ImZyb20iOjgwMDAsInRvIjoyNTAwMH0&p=2&q=%D0%BE%D0%B1%D0%BC%D0%B5%D0%BD&s=104&user=1'
# soup = get_bs4_content(url, headless=False)
# pages = get_quanity_pages(soup)
# print (f'Страниц найдено - {len(pages)+1}')
# with open ('links.txt', 'w') as f:
#     f.close()
# for page in pages:
#     with open ('links.txt', 'a') as f:
#         f.write(page+'\n')
#
#     print (page)



