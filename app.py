import asyncio

import aioschedule

from add_links_lite import work_with_links
from avito_parcer_script import myphones_get_avarage_prices, update_archive, mycars_get_avarage_prices
from keyboards.inline.choice_buttons import next_link_buttons, main_menu
from archive import archive_status


async def on_startup(_):
    user_should_be_notified = 324029452  # Наверное это должны быть вы сами? Как всезнающий админ:)
    asyncio.create_task(scheduler())
    await bot.send_message(user_should_be_notified, 'Бот запущен', reply_markup=main_menu)

async def choose_your_dinner():
    await bot.send_message(chat_id=324029452, text='---------------')
    outputs = myphones_get_avarage_prices()
    for output in outputs:
        await bot.send_message(chat_id=324029452, text=output)

async def update_my_archive():
    await bot.send_message(chat_id=324029452, text='---------------')
    amount_of_keys = 30
    update_archive(amount_of_keys)
    amount = archive_status()
    await bot.send_message(chat_id=324029452, text=f'Обновлено {amount_of_keys} позиций из {amount}')
async def add_links():
    new_links_quanity, msg = work_with_links()
    await bot.send_message(chat_id=324029452, text=f'Добавлено {new_links_quanity} ссылок')
    await bot.send_message(chat_id=324029452, text=msg, disable_web_page_preview=True, reply_markup=next_link_buttons)

async def check_auto():
    await bot.send_message(chat_id=324029452, text='Добавляем ссылки')
    outputs = mycars_get_avarage_prices()
    with open('data/auto_average.txt', 'a', encoding='UTF-8') as f:
        f.writelines(f'{outputs[-1].split()[-1].strip()}\n')
    await bot.send_message(chat_id=324029452, text=outputs[-1])

async def scheduler():
    aioschedule.every().day.at("03:00").do(choose_your_dinner)
    aioschedule.every().day.at("05:00").do(update_my_archive)
    aioschedule.every().day.at("07:00").do(add_links)
    #aioschedule.every().hour.at(':03').do(check_auto)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp
    from loader import bot


    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)