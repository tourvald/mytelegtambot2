from loader import dp
from aiogram.types import Message
import datetime

distance = rub_per_km = use_time = 0
def show_car_data():
    rub = 0
    km = []
    with open('data/nexia.txt', 'r', encoding='utf-8') as f:  # Открываем файл архива для чтения
        myfile = f.readlines()
        f.close()
    for line in myfile:
        string = line.split(' ')
        if len(string) < 2:
            pass
        elif string[1] in {'/бензин', '/мойка','/омывайка','/штраф','/ремонт',}:
            rub = rub + int(string[2])
        elif string[1] == '/пробег':
            km.append(int(string[2]))
    distance = (km[-1] - km[0])
    rub_per_km = round(rub / distance, 2)
    use_time = (datetime.datetime.strptime(string[0], '%Y-%m-%d') - datetime.datetime.strptime(myfile[1][:10], '%Y-%m-%d')).days
    print (datetime.datetime.strptime(string[0], '%Y-%m-%d') - datetime.datetime.strptime(myfile[1][:10], '%Y-%m-%d'))
    month_spendings = round(rub / use_time * 30.4)
    msg = f'На Нексии пройдено - {distance}км\nСтоимость километра - {rub_per_km}р\nТраты в месяц - {month_spendings}р\n\
В использовании - {use_time} дней'
    return (msg)

def add_car_data(a,b):
    with open('data/nexia.txt', 'a', encoding='utf-8') as f: #Открываем файл архива для чтения
        f.write(f'\n{a} {b}')
        f.close() #Закрываем файл
        show_car_data()

@dp.message_handler(commands=['пробег'])
async def process_command_price(message: Message):
    add_car_data(datetime.date.today(), message.text)
    await message.answer(show_car_data())

@dp.message_handler(commands=['мойка'])
async def process_command_price(message: Message):
    add_car_data(datetime.date.today(), message.text)
    await message.answer(show_car_data())

@dp.message_handler(commands=['омывайка'])
async def process_command_price(message: Message):
    add_car_data(datetime.date.today(), message.text)
    await message.answer(show_car_data())

@dp.message_handler(commands=['бензин'])
async def process_command_price(message: Message):
    add_car_data(datetime.date.today(), message.text)
    await message.answer(show_car_data())

@dp.message_handler(commands=['ремонт'])
async def process_command_price(message: Message):
    add_car_data(datetime.date.today(), message.text)
    await message.answer(show_car_data())

@dp.message_handler(commands=['штраф'])
async def process_command_price(message: Message):
    add_car_data(datetime.date.today(), message.text)
    await message.answer(show_car_data())

@dp.message_handler(commands=['авто'])
async def process_command_price(message: Message):
    await message.answer(show_car_data())