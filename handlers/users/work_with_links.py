from loader import dp
from aiogram.types import Message
from multiprocessing import Pool
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import Message, CallbackQuery
from loader import dp, bot
from make_filtered_links import add_links_to_db, get_new_items, get_new_items_lite
from work_with_links import count_links_quanity
import datetime

keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Поддходит",
                                 callback_data='next:yes'
                                 ),
            InlineKeyboardButton(text="Не подходит",
                                 callback_data='next:no'
                                 )
        ]]
)


@dp.message_handler(commands=['обмен'])
async def initiate_work_with_links(message: Message):
    '''начало работы с ссылками, переводит в замкнутый блок CallBackQuery'''
    with open('new_links.txt', 'r') as f:
        string = f.readlines()
    msg = string[0]
    string.pop(0)
    with open('new_links.txt', 'w') as f:
        f.writelines(string)
    await bot.send_message(text=msg, reply_markup=keyboard, chat_id=message.chat.id, disable_web_page_preview = True)

@dp.callback_query_handler(text_contains='next')
async def working_with_links(call: CallbackQuery):

    with open ('working_link', 'r', encoding='UTF-8') as f:
        link_to_add = f.readline()
    if 'yes' in call.data:
        with open ('data/neuro_learn/yes_links.txt', 'a', encoding='utf-8') as f:
            f.writelines(link_to_add)
        print('Ссылка подходит')
    if 'no' in call.data:
        with open ('data/neuro_learn/no_links.txt', 'a', encoding='utf-8') as f:
            f.writelines(link_to_add)
        print ('Ссылка не подходит' + link_to_add)

    with open('new_links.txt', 'r') as f:
        string = f.readlines()
    msg = string[0]
    string.pop(0)
    with open ('new_links.txt', 'w') as f:
        f.writelines(string)
    with open ('working_link', 'w', encoding='UTF-8') as f:
        f.writelines(msg)
    await bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
    await call.message.answer(text=str(len(string))+':'+msg, reply_markup=keyboard, disable_web_page_preview=True)

@dp.message_handler(commands=['add_links'])
async def initiate_work_with_links(message: Message):
    processes_ = None
    if len(message.text.split(' ')) > 1:
        processes_ = int(message.text.split(' ')[1])
    '''добавляет новые ссылки с объявлениями по обменам за вчерашний день'''
    with open('item_links.txt', 'w') as f:
        f.close()

    urls = [
    'https://www.avito.ru/moskva/telefony/mobile-ASgBAgICAUSwwQ2I_Dc?f=ASgBAQECAUSwwQ2I_DcBQOjrDjT~_dsC_P3bAvr92wIBRcaaDBh7ImZyb20iOjgwMDAsInRvIjo1MDAwMH0&q=обмен&s=104&user=1',
    'https://www.avito.ru/moskva/audio_i_video/televizory_i_proektory/televizory-ASgBAgICAkSIArgJ0sENkLA5?f=ASgBAQICAkSIArgJ0sENkLA5AUDqvA0U_NE0&q=обмен&s=104&user=1',
    'https://www.avito.ru/moskva/audio_i_video/naushniki-ASgBAgICAUSIAtRO?cd=1&f=ASgBAQICAUSIAtROAUDqvA0U_NE0&q=обмен&s=104&user=1',
    'https://www.avito.ru/moskva/planshety_i_elektronnye_knigi?cd=1&f=ASgCAQICAUD0vA0UkNI0&q=обмен&s=104&user=1',
    'https://www.avito.ru/moskva/igry_pristavki_i_programmy/igrovye_pristavki-ASgBAgICAUSSAsoJ?f=ASgBAQICAUSSAsoJAUDsvA0UgNI0&q=обмен&s=104&user=1',
    'https://www.avito.ru/moskva/sport_i_otdyh/drugoe-ASgBAgICAUTKAuIK?f=ASgBAQICAUTKAuIKAUCIvQ0UuNI0&q=электросамокат+обмен&s=104&user=1',
    'https://www.avito.ru/moskva/nastolnye_kompyutery?f=ASgCAQICAUDuvA0UhNI0&q=mac+обмен&s=104&user=1'
    ]
    p = Pool(processes=processes_)
    p.map(get_new_items, urls)

    with open ('item_links.txt', 'r') as f:
        item_links = f.readlines()
    with open ('old_links.txt', 'r') as f:
        old_links = f.readlines()
    links_to_add = set(item_links) - set(old_links)
    with open('old_links.txt', 'w') as f:
        f.writelines(item_links)
    with open ('new_links.txt', 'a') as f:
        f.writelines(links_to_add)
    await bot.send_message(text=f'Ссылки добавлены. Сейчас {len(links_to_add)}', chat_id=message.chat.id, disable_web_page_preview = True)


@dp.message_handler(commands=['add_links_lite'])
async def initiate_work_with_links(message: Message):
    processes_ = None
    if len(message.text.split(' ')) > 1:
        processes_ = int(message.text.split(' ')[1])
    '''добавляет новые ссылки с объявлениями по обменам за вчерашний день'''
    with open('item_links.txt', 'w') as f:
        f.close()

    urls = [
        'https://www.avito.ru/moskva/telefony/mobile-ASgBAgICAUSwwQ2I_Dc?f=ASgBAQECAUSwwQ2I_DcBQOjrDjT~_dsC_P3bAvr92wIBRcaaDBh7ImZyb20iOjgwMDAsInRvIjo1MDAwMH0&q=обмен&s=104&user=1',
        'https://www.avito.ru/moskva/audio_i_video/televizory_i_proektory/televizory-ASgBAgICAkSIArgJ0sENkLA5?f=ASgBAQICAkSIArgJ0sENkLA5AUDqvA0U_NE0&q=обмен&s=104&user=1',
        'https://www.avito.ru/moskva/audio_i_video/naushniki-ASgBAgICAUSIAtRO?cd=1&f=ASgBAQICAUSIAtROAUDqvA0U_NE0&q=обмен&s=104&user=1',
        'https://www.avito.ru/moskva/planshety_i_elektronnye_knigi?cd=1&f=ASgCAQICAUD0vA0UkNI0&q=обмен&s=104&user=1',
        'https://www.avito.ru/moskva/igry_pristavki_i_programmy/igrovye_pristavki-ASgBAgICAUSSAsoJ?f=ASgBAQICAUSSAsoJAUDsvA0UgNI0&q=обмен&s=104&user=1',
        'https://www.avito.ru/moskva/sport_i_otdyh/drugoe-ASgBAgICAUTKAuIK?f=ASgBAQICAUTKAuIKAUCIvQ0UuNI0&q=электросамокат+обмен&s=104&user=1',
        'https://www.avito.ru/moskva/nastolnye_kompyutery?f=ASgCAQICAUDuvA0UhNI0&q=mac+обмен&s=104&user=1'
    ]
    p = Pool(processes=1)
    p.map(get_new_items_lite, urls)

    with open('item_links.txt', 'r') as f:
        item_links = f.readlines()
    with open('old_links.txt', 'r') as f:
        old_links = f.readlines()
    links_to_add = set(item_links) - set(old_links)
    with open('old_links.txt', 'w') as f:
        f.writelines(item_links)
    with open('new_links.txt', 'a') as f:
        f.writelines(links_to_add)
    await bot.send_message(text=f'Ссылки добавлены. Сейчас {len(links_to_add)}', chat_id=message.chat.id,
                           disable_web_page_preview=True)


@dp.message_handler(content_types=['document'])
async def get_photo(message: Message):
    await message.document.download()
    with open ('new_links.txt', 'r') as f:
        new_links = f.readlines()
    print (new_links)
    with open ('item_links.txt', 'a') as f:
        f.writelines(new_links)