import os

import river_house
import platform

# Определяем в какой системе мы находимся и задаем параметр для спуска в корневую дирректорию
print (platform.processor())
if platform.processor() == 'Intel64 Family 6 Model 42 Stepping 7, GenuineIntel':
	chdir_path = '../..'
else:
	chdir_path = '..'

os.chdir(chdir_path)
print (f'rh_run:{os.getcwd()}')
# river_house