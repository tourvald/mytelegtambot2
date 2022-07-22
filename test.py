import os
from dotenv import load_dotenv

from sys import platform
print (platform)

if platform == "linux" or platform == "linux2":
    print (platform)
elif platform == "darwin":
    print (platform)
elif platform == "win32":
    print (platform)

load_dotenv()
PATH_TO_WEBDRIVER_MAC = os.getenv("PATH_TO_WEBDRIVER_MAC")
print(PATH_TO_WEBDRIVER_MAC)