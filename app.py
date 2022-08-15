import asyncio
from multiprocessing import Pool

import aioschedule

from avito_parcer_script import myphones_get_avarage_prices
from handlers.users.purchase import myphones_prices
from handlers.users.work_with_links import initiate_work_with_links
from make_filtered_links import get_new_items_lite


async def on_startup(_):
    user_should_be_notified = 324029452  # Наверное это должны быть вы сами? Как всезнающий админ:)
    asyncio.create_task(scheduler())
    await bot.send_message(user_should_be_notified, 'Бот запущен')

async def choose_your_dinner():
    outputs = myphones_get_avarage_prices()
    for output in outputs:
        await bot.send_message(chat_id=324029452, text=output)

async def scheduler():
    aioschedule.every().day.at("15:33").do(choose_your_dinner)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp
    from loader import bot


    # @dp.message_handler()
    # async def choose_your_dinner():
    #     await bot.send_message(chat_id=324029452, text="Хей🖖 не забудьвыбрать свой ужин сегодня",)


    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)