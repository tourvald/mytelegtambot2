import asyncio
import os
import subprocess


import aioschedule
import os
import avito_parcer_script

from add_links_lite import work_with_links
from avito_parcer_script import myphones_get_avarage_prices, update_archive, write_car_data
from my_libs.river_house.river_house import rh_parce
from keyboards.inline.choice_buttons import next_link_buttons, main_menu
from archive import archive_status
import time
import os

current_directory = os.getcwd()
print(f"Текущая директория: {current_directory}")

async def on_startup(_):
    user_should_be_notified = 324029452  # Наверное это должны быть вы сами? Как всезнающий админ:)
    asyncio.create_task(scheduler())
    print('Бот онлайн')
    await bot.send_message(user_should_be_notified, 'Бот запущен', reply_markup=main_menu)

async def choose_your_dinner():
    print(time.perf_counter())
    await bot.send_message(chat_id=324029452, text='---------------')
    outputs = myphones_get_avarage_prices()
    print(time.perf_counter())
    for output in outputs:
        await bot.send_message(chat_id=324029452, text=output)

async def restart():
    os.system('shutdown -r -t 0')

async def update_my_archive():
    await bot.send_message(chat_id=324029452, text='---------------')
    amount_of_keys = 20
    avito_parcer_script.update_archive(amount_of_keys)
    amount = archive_status()
    await bot.send_message(chat_id=324029452, text=f'Обновлено {amount_of_keys} позиций из {amount}')
async def add_links():
    new_links_quanity, msg = work_with_links()
    await bot.send_message(chat_id=324029452, text=f'Добавлено {new_links_quanity} ссылок')
    await bot.send_message(chat_id=324029452, text=msg, disable_web_page_preview=True, reply_markup=next_link_buttons)

async def add_car_data():
    write_car_data()
    print('Данные авто добавлены')

# async def currency_parce_today():
#     # Получаем абсолютный путь к скрипту
#     script_path = os.path.join('my_libs', 'currency', 'main.py')
#     # Запускаем скрипт как отдельный процесс
#     process = subprocess.Popen(['python', script_path], cwd=os.path.dirname(script_path))
#     print('Ривер хаус парсинг завершен')


async def scheduler():
    #aioschedule.every().day.at("03:10").do(choose_your_dinner)
    aioschedule.every().day.at("13:59").do(update_my_archive)
    aioschedule.every().day.at("04:55").do(restart)
    # aioschedule.every().day.at("16:01").do(currency_parce_today)
    aioschedule.every(1).hours.at(":41").do(add_car_data)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp
    from loader import bot

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)