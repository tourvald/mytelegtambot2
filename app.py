import asyncio
import aioschedule
from avito_parcer_script import myphones_get_avarage_prices, update_archive, avito_auto_parce_soup, get_soup_for_avito_parce, avito_parce_soup
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
    await bot.send_message(chat_id=324029452, text='Добавляем ссылки')
    outputs = myphones_get_avarage_prices()
    for output in outputs:
        await bot.send_message(chat_id=324029452, text=output)

async def update_my_archive():
    await bot.send_message(chat_id=324029452, text='Обновляем базу')
    amount_of_keys = 30
    update_archive(amount_of_keys)
    await bot.send_message(chat_id=324029452, text=f'Обновлено {amount_of_keys} позиций')
async def add_links():
    new_links_quanity, msg = work_with_links()
    await bot.send_message(chat_id=324029452, text=f'Добавлено {new_links_quanity} ссылок')
    await bot.send_message(chat_id=324029452, text=msg, disable_web_page_preview=True, reply_markup=next_link_buttons)

async def check_auto():
    soup = get_soup_for_avito_parce('https://www.avito.ru/moskva/avtomobili?f=ASgBAQECA0Tgtg24mSjitg2IrSjqtg3A8SgBQPC2DRTstygBRfgCGXsiZnJvbSI6MTk3NzUsInRvIjoxOTc3NX0&q=Volkswagen+Polo%2C+2017%2C+механика&radius=0&s=104')
    price, search_request = avito_auto_parce_soup(soup)
    price_std, search_request = avito_parce_soup(soup)
    with open('auto.txt', 'a', encoding='UTF-8') as f:
        f.writelines(f'{price}, {price_std}, {search_request}\n')
    await bot.send_message(chat_id=324029452, text=f'{price}, {price_std}, {search_request}\n')

async def scheduler():
    aioschedule.every().day.at("04:00").do(choose_your_dinner)
    aioschedule.every().day.at("01:46").do(update_my_archive)
    aioschedule.every().day.at("08:00").do(add_links)
    aioschedule.every().hour.at(':51').do(check_auto)
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