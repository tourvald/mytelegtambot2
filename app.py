import asyncio
import aioschedule
from avito_parcer_script import myphones_get_avarage_prices
from add_links_lite import work_with_links
from my_libs.big_geek_parce import get_price_from_site
from keyboards.inline.choice_buttons import next_link_buttons, main_menu
from avito_parcer_script import parce_page
from my_libs.libs_selenium import create_chrome_driver_object
from mylibs import get_bs4_from_driver


async def on_startup(_):
    user_should_be_notified = 324029452  # Наверное это должны быть вы сами? Как всезнающий админ:)
    asyncio.create_task(scheduler())
    await bot.send_message(user_should_be_notified, 'Бот запущен', reply_markup=main_menu)

async def choose_your_dinner():
    outputs = myphones_get_avarage_prices()
    for output in outputs:
        await bot.send_message(chat_id=324029452, text=output)

async def add_links():
    new_links_quanity, msg = work_with_links()
    await bot.send_message(chat_id=324029452, text=f'Добавлено {new_links_quanity} ссылок')
    await bot.send_message(chat_id=324029452, text=msg, disable_web_page_preview=True, reply_markup=next_link_buttons)


async def scheduler():
    aioschedule.every().day.at("04:00").do(choose_your_dinner)
    aioschedule.every().day.at("08:00").do(add_links)
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