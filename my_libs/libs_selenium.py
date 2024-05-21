import json
import os
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


class BrowserAutomation:
    COOKIES_FILE_PATH = 'utils/cookies1.json'
    PROFILE_PATH = '/Users/dmitrijkozuskevic/Library/Application Support/Google/Chrome/Default'  # macOS пример

    def __init__(self, profile_path=None):
        self.profile_path = profile_path or self.PROFILE_PATH
        self.driver = self.init_driver(self.profile_path)
        self.cookies_file_path = self.COOKIES_FILE_PATH
        self.cookies = self.load_cookies(self.cookies_file_path)
        self.user_agent = self.get_random_user_agent()
        self.apply_cookies_and_user_agent()

    @staticmethod
    def load_cookies(file_path):
        if not os.path.exists(file_path):
            print(f"Файл куки не найден: {file_path}")
            return []

        try:
            with open(file_path, 'r') as file:
                cookies = json.load(file)
            return cookies
        except (json.JSONDecodeError, IOError) as e:
            print(f"Ошибка при загрузке куки: {e}")
            return []

    @staticmethod
    def save_cookies(driver, file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Создание каталога, если его не существует
        cookies = driver.get_cookies()
        with open(file_path, 'w') as file:
            json.dump(cookies, file)

    @staticmethod
    def get_random_user_agent():
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
        ]
        return random.choice(user_agents)

    def init_driver(self, profile_path):
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument(f"user-agent={self.get_random_user_agent()}")
        if profile_path:
            try:
                options.add_argument(f"user-data-dir={profile_path}")  # Использование реального профиля браузера
            except Exception as e:
                print(f"Не удалось загрузить профиль браузера: {e}")
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        return driver

    def apply_cookies_and_user_agent(self):
        # Загружаем страницу Avito для установки куки и пользовательского агента
        self.driver.get("https://www.avito.ru")

        # Устанавливаем куки
        for cookie in self.cookies:
            self.driver.add_cookie({
                'name': cookie['name'],
                'value': cookie['value'],
                'domain': cookie.get('domain', '.avito.ru')
            })

        # Устанавливаем пользовательский агент
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": self.user_agent})

    @staticmethod
    def get_page_with_delay(driver, url):
        driver.get(url)
        time.sleep(random.uniform(1, 5))  # Задержка между запросами

    @staticmethod
    def emulate_user_interaction(driver):
        actions = ActionChains(driver)
        actions.move_by_offset(random.randint(0, 100), random.randint(0, 100)).perform()
        time.sleep(random.uniform(0.5, 1.5))
        actions.move_by_offset(random.randint(0, 100), random.randint(0, 100)).perform()
        time.sleep(random.uniform(0.5, 1.5))
        actions.click().perform()
        time.sleep(random.uniform(0.5, 1.5))
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
        time.sleep(random.uniform(0.5, 1.5))

    def fetch_html(self, url):
        # Переходим на целевую страницу
        self.get_page_with_delay(self.driver, url)
        self.emulate_user_interaction(self.driver)
        return self.driver.page_source

    def get_bs4_objects(self, urls):
        bs4_objects = []
        for url in urls:
            page_source = self.fetch_html(url)
            soup = BeautifulSoup(page_source, 'html.parser')
            bs4_objects.append(soup)
            if not os.path.exists(self.cookies_file_path):
                self.save_cookies(self.driver, self.cookies_file_path)
            time.sleep(random.uniform(1, 3))  # Задержка между запросами
        return bs4_objects

    def extract_titles(self, bs4_objects):
        titles = [soup.title.string if soup.title else 'No title found' for soup in bs4_objects]
        return titles

    def close(self):
        self.driver.quit()


# Пример использования
if __name__ == "__main__":
    # Создание экземпляра BrowserAutomation
    browser = BrowserAutomation()

    # Список URL-адресов для получения заголовков
    urls = [
        "https://www.avito.ru/all/telefony/mobilnye_telefony/apple/iphone_14_pro_max/128_gb-ASgBAgICBESywA3YjuUQtMANzqs5sMENiPw35uAN9sFc?f=ASgBAQICBESywA3YjuUQtMANzqs5sMENiPw35uAN9sFcAUDo6w40_v3bAvz92wL6_dsC&q=iPhone+14+Pro+Max+128&s=104",
        "https://www.avito.ru/moskva_i_mo/telefony/mobilnye_telefony/apple/iphone_15_pro_max/256_gb-ASgBAgICBESywA3Woe0RtMANzqs5sMENiPw35uAN~MFc?f=ASgBAQICBESywA3Woe0RtMANzqs5sMENiPw35uAN~MFcAUDo6w40_v3bAvz92wL6_dsC&q=iPhone+15+Pro+Max+256",
        "https://www.avito.ru/moskva/telefony/mobilnye_telefony/apple-ASgBAgICAkS0wA3OqzmwwQ2I_Dc?cd=1&f=ASgBAQICA0SywA3yvcgBtMANzqs5sMENiPw3AkDm4A0U9sFc6OsONP792wL8_dsC~v3bAg&q=iphone+13+pro+max+128&s=104&user=1",
        "https://www.avito.ru/moskva/telefony/mobilnye_telefony/apple-ASgBAgICAkS0wA3OqzmwwQ2I_Dc?bt=1&cd=1&f=ASgBAQICA0SywA2MgTy0wA3OqzmwwQ2I_DcDQPa8DRSU0jTm4A0U9sFc6OsONP792wL8_dsC~v3bAg&q=iphone+12+pro+max+128&s=104&user=1"
    ]

    # Получение объектов BeautifulSoup для всех URL-адресов
    bs4_objects = browser.get_bs4_objects(urls)

    # Извлечение заголовков из объектов BeautifulSoup
    titles = browser.extract_titles(bs4_objects)
    for title in titles:
        print(f"Заголовок страницы: {title}")

    # Закрытие драйвера

    # browser.init_driver(browser.PROFILE_PATH)

    browser.close()