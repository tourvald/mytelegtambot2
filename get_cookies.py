from selenium import webdriver
import pickle
import time
from my_libs.libs_selenium import create_chrome_driver_object
def save_cookies(url):
    driver = create_chrome_driver_object(headless=False, proxy=None)
    try:
        driver.get(url)
        file_name = url.strip('https://').split('.')[-2]
        print(file_name)
        input_=input('Сохранить куки? y/n')
        if input_ == 'y':
            with open('test_cookies2.pkl', 'wb') as f:
               f.close()
            pickle.dump(driver.get_cookies(), open(f'cookies/{file_name}.pkl', 'wb'))

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()

def check_cookies(url):
    driver = create_chrome_driver_object(headless=False, proxy=None)
    driver.get(url)
    driver.implicitly_wait(10)
    time.sleep(3)
    file_name = url.strip('https://').split('.')[-2]
    print(file_name)
    try:
        cookies = pickle.load(open(f'cookies/{file_name}.pkl', 'rb'))
        print(cookies)
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.refresh()
        time.sleep(3)
        print('Куки загрузились')
        input_=input('Загрузились куки? y/n')
        if input_ == 'y':
            print('Спасибо')
    except Exception as e:
        print(e)
    finally:
        driver.close()
        driver.quit()

url = 'https://web.telegram.org'
# url = 'https://www.avito.ru'
# url = 'https://youla.ru/'
# save_cookies(url)
check_cookies(url)