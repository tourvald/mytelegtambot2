import os

from river_house import rh_parce
from river_house_total import river_house_total_2, separatate_first_column
import platform

# Определяем в какой системе мы находимся и задаем параметр для спуска в корневую дирректорию
print (platform.processor())
if platform.processor() == 'Intel64 Family 6 Model 42 Stepping 7, GenuineIntel':
	chdir_path = '../..'
else:
	chdir_path = '..'

os.chdir(chdir_path)
print (f'rh_run:{os.getcwd()}')
def rh_run():
	rh_parce()
	river_house_total_2()
	separatate_first_column()

if __name__ == "__main__":
	# os.chdir('..')
	print(os.getcwd())
	rh_run()
