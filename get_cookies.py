from selenium import webdriver
import pickle
import time


# options
options = webdriver.ChromeOptions()

# user-agent
options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")

# disable webdriver mode

# # for older ChromeDriver under version 79.0.3945.16
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option("useAutomationExtension", False)

# for ChromeDriver version 79.0.3945.16 or over
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(
    executable_path="settings/chromedriver_mac",
    options=options
)

# "C:\\users\\selenium_python\\chromedriver_mac\\chromedriver_mac.exe"
# r"C:\users\selenium_python\chromedriver_mac\chromedriver_mac.exe"

try:
    driver.get("https://avito.ru")


    time.sleep(170)
    with open('test_cookies.pkl', 'wb') as f:
       f.close()
    pickle.dump(driver.get_cookies(), open('cookies/test_cookies.pkl', 'wb'))

    # time.sleep(4)
    # cookies = pickle.load(open('cookies/test_cookies.pkl', 'rb'))
    # for cookie in cookies:
    #     driver.add_cookie(cookie)
    # time.sleep(3)
    # print('Куки загрузились')
    # driver.refresh()
    # time.sleep(10)

except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()