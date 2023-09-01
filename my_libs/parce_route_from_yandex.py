from my_libs.libs_selenium import create_chrome_driver_object
from mylibs import get_bs4_from_driver
import datetime
import os
def get_route_time(route_url:str) -> int:
    driver = create_chrome_driver_object()
    soup = get_bs4_from_driver(driver, route_url)
    try:
        time = soup.find('div', {'class': 'auto-route-snippet-view__route-title-primary'}).text
        if len(time.split()) < 3:
            print(len(time.split()))
            minutes = time.split()[0]
            return minutes
        elif len(time.split()) > 2:
            print(len(time.split()))
            hours = int(time.split()[0])
            minutes = int(time.split()[2])
            total_minutes = minutes + hours * 60
            return_ = total_minutes
    except Exception as e:
        print(e)
        return_ = 'get_route_time_error'
    return return_



if __name__ == '__main__':
    os.chdir('..')
    url = 'https://yandex.ru/maps/213/moscow/?ll=37.694640%2C55.870934&mode=routes&rtext=55.786946%2C37.621058~55.961339%2C38.042808&rtt=auto&ruri=~ymapsbm1%3A%2F%2Fgeo%3Fdata%3DCgg1MzA2MzEzNhJB0KDQvtGB0YHQuNGPLCDQnNC%2B0YHQutC%2B0LLRgdC60LDRjyDQvtCx0LvQsNGB0YLRjCwg0KTRgNGP0LfQuNC90L4iCg3XKxhCFWrYX0I%3D&z=11.27'
    # url = 'https://yandex.ru/maps/213/moscow/?ll=37.694640%2C55.870934&mode=routes&rtext=55.941979%2C37.490244~55.786946%2C37.621058&rtt=auto&ruri=~&z=11'
    time = get_route_time(url)
    print(time)
    # today = datetime.datetime.today().date().day
    # today = today - 9
    # print(today)