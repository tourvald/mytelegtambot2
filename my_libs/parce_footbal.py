from my_libs.libs_selenium import create_chrome_driver_object
from mylibs import get_bs4_from_driver
import os

def get_yellow_cards_for_10_matches(url:str) -> int:
    driver = create_chrome_driver_object(headless=False)
    soup = get_bs4_from_driver(driver, url)
    try:
        team = get_match_title(soup)
        links_to_parce = get_links_to_parce(soup)
        yellow_cards = get_yellow_cards(driver, links_to_parce, team)
    except Exception as e:
        print(e)
        return_ = 'get_route_time_error'
    return None

def get_match_title(soup):
    return soup.find('div', {'class': 'heading__name'}).text

def get_links_to_parce(soup):
    return_ = []
    div_with_urls = soup.find_all('div', {'class': 'sportName'})
    # print(len(div_with_urls))
    # for div in div_with_urls:
    #     print(div.text)
    div_with_urls = div_with_urls[-2]
    urls_ids = div_with_urls.find_all('div', {'title': 'Подробности матча!'})
    for url_id in urls_ids:
        return_.append('https://www.flashscore.ru.com/match/'+url_id.get('id').strip('g_1_'))
    # for ret in return_:
    #     print(ret)
    return return_

def get_yellow_cards(driver, links_to_parce, team):
    total_yellow_cards = 0
    for url in links_to_parce:
        print(url)
        soup = get_bs4_from_driver(driver, url)
        home = soup.find('div', {'class': 'duelParticipant__home'})
        away = soup.find('div', {'class': 'duelParticipant__away'})
        yellow_cards = 0
        if team in home.text:
            side = 'smv__homeParticipant'
        if team in away.text:
            side = 'smv__awayParticipant'

        cards = soup.find_all('div', {'class': side})
        for card in cards:
            if card.find('svg', {'class': 'card-ico'}):
                yellow_cards += 1
        total_yellow_cards = total_yellow_cards + yellow_cards

        print(yellow_cards)
    print(total_yellow_cards, total_yellow_cards/10)
        # break


if __name__ == '__main__':
    os.chdir('..')
    # url = 'https://www.flashscore.ru.com/team/bayern-munich/nVp0wiqd/'
    url = 'https://www.flashscore.ru.com/team/a-lustenau/655zEcZJ/'
    get_yellow_cards_for_10_matches(url)