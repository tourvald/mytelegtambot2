from loader import dp
from aiogram.types import Message
from multiprocessing import Pool
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import Message, CallbackQuery
from loader import dp, bot
from keyboards.inline.choice_buttons import next_link_buttons
from work_with_links import count_links_quanity
import datetime



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

    with open ('data/work_with_links/working_link', 'r', encoding='UTF-8') as f:
        link_to_add = f.readline()
    if 'yes' in call.data:
        with open ('data/neuro_learn/yes_links.txt', 'a', encoding='utf-8') as f:
            f.writelines(link_to_add)
        print('Ссылка подходит')
    if 'no' in call.data:
        with open ('data/neuro_learn/no_links.txt', 'a', encoding='utf-8') as f:
            f.writelines(link_to_add)
        print ('Ссылка не подходит' + link_to_add)

    with open('data/work_with_links/new_links.txt', 'r') as f:
        string = f.readlines()
    msg = string[0]
    string.pop(0)
    with open ('data/work_with_links/new_links.txt', 'w') as f:
        f.writelines(string)
    with open ('data/work_with_links/working_link', 'w', encoding='UTF-8') as f:
        f.writelines(msg)
    await bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
    await call.message.answer(text=str(len(string))+':'+msg, reply_markup=next_link_buttons, disable_web_page_preview=True)

@dp.message_handler(commands=['add_links'])
async def initiate_work_with_links(message: Message):
    '''добавляет новые ссылки с объявлениями по обменам за вчерашний день'''
    with open('item_links.txt', 'w', encoding='UTF-8') as f:
        f.close()
    with open('data/links_to_parce.txt', 'r', encoding='UTF-8') as f:
        urls = f.readlines()

    p = Pool(processes=1)
    p.map(get_new_items_lite, urls)

    with open('item_links.txt', 'r', encoding='UTF-8') as f:
        item_links = f.readlines()
    with open('old_links.txt', 'r', encoding='UTF-8') as f:
        old_links = f.readlines()
    links_to_add = set(item_links) - set(old_links)
    with open('old_links.txt', 'w', encoding='UTF-8') as f:
        f.writelines(item_links)
    with open('new_links.txt', 'a', encoding='UTF-8') as f:
        f.writelines(links_to_add)
    await bot.send_message(text=f'Добавлено {len(links_to_add)} ссылки', chat_id=324029452,
                           disable_web_page_preview=True)
    with open('new_links.txt', 'r', encoding='UTF-8') as f:
        string = f.readlines()
    msg = string[0]
    string.pop(0)
    with open('new_links.txt', 'w', encoding='UTF-8') as f:
        f.writelines(string)
    await bot.send_message(text=str(len(string)) + ':' + msg, reply_markup=keyboard, chat_id=324029452,
                           disable_web_page_preview=True)


@dp.message_handler(commands=['add_links_lite'])
async def initiate_work_with_links(message: Message):
    processes_ = None
    if len(message.text.split(' ')) > 1:
        processes_ = int(message.text.split(' ')[1])
    '''добавляет новые ссылки с объявлениями по обменам за вчерашний день'''
    with open('item_links.txt', 'w', encoding='UTF-8') as f:
        f.close()
    with open('data/links_to_parce.txt', 'r', encoding='UTF-8') as f:
        urls = f.readlines()

    p = Pool(processes=1)
    p.map(get_new_items_lite, urls)

    with open('item_links.txt', 'r', encoding='UTF-8') as f:
        item_links = f.readlines()
    with open('old_links.txt', 'r', encoding='UTF-8') as f:
        old_links = f.readlines()
    links_to_add = set(item_links) - set(old_links)
    with open('old_links.txt', 'w', encoding='UTF-8') as f:
        f.writelines(item_links)
    with open('new_links.txt', 'a', encoding='UTF-8') as f:
        f.writelines(links_to_add)
    await bot.send_message(text=f'Добавлено {len(links_to_add)} ссылки', chat_id=message.chat.id,
                           disable_web_page_preview=True)
    with open('new_links.txt', 'r', encoding='UTF-8') as f:
        string = f.readlines()
    msg = string[0]
    string.pop(0)
    with open('new_links.txt', 'w', encoding='UTF-8') as f:
        f.writelines(string)
    await bot.send_message(text=str(len(string))+':'+msg, reply_markup=keyboard, chat_id=message.chat.id, disable_web_page_preview = True)