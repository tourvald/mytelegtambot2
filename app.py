import asyncio
import os
import aioschedule
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.bot import DefaultBotProperties
from config import BOT_TOKEN

import avito_parcer_script
from add_links_lite import work_with_links
from avito_parcer_script import myphones_get_avarage_prices, update_archive, write_car_data_2
from my_libs.river_house.river_house import rh_parce
from archive import archive_status
from handlers.users.purchase import purchase_router

# Инициализация бота с параметрами по умолчанию
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Регистрация маршрутизатора
dp.include_router(purchase_router)

async def restart():
    os.system('shutdown -r -t 0')

async def update_my_archive():
    await bot.send_message(chat_id=324029452, text='---------------')
    amount_of_keys = 5
    avito_parcer_script.update_archive(amount_of_keys)
    amount = archive_status()
    await bot.send_message(chat_id=324029452, text=f'Обновлено {amount_of_keys} позиций из {amount}')

async def add_car_data():
    write_car_data_2()
    print('Данные авто добавлены')

async def rh_parce_today():
    rh_parce()
    print('Ривер хаус парсинг завершен')

async def scheduler():
    aioschedule.every().day.at("04:35").do(update_my_archive)
    aioschedule.every().day.at("04:55").do(restart)
    aioschedule.every().day.at("04:21").do(rh_parce_today)
    aioschedule.every(3).hours.at(":00").do(add_car_data)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

async def on_startup():
    user_should_be_notified = 324029452  # Наверное это должны быть вы сами? Как всезнающий админ:)
    asyncio.create_task(scheduler())
    print('Бот онлайн')
    await bot.send_message(user_should_be_notified, 'Бот запущен')

async def main():
    await on_startup()
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
