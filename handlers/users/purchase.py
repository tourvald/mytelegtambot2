import datetime
import json
import os
import time
from multiprocessing import Pool

import avito_parcer_script
from my_libs.big_geek_parce import get_price_from_site
from add_links_lite import work_with_links
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import Message, CallbackQuery
from my_libs.myphones_lib import get_last_3_months_report
import archive
from avito_parcer_script import myphones_get_avarage_prices, get_soup_for_avito_parce, avito_parce_soup, parce_page
from keyboards.inline.choice_buttons import choice, admin, cancel_button, next_link_buttons, main_menu
from keyboards.inline.equipment import box, charger, check, scratches, chips
from loader import dp, bot
from my_libs.libs_selenium import create_chrome_driver_object

ti = 0
data = {}
class FSM_change_link(StatesGroup):
    waiting_for_new_link = State()

class FSM_waiting_for_torrent(StatesGroup):
    waiting_for_torrent = State()

class FSM_buy_phone(StatesGroup):
    equipment = State()


@dp.message_handler(commands=['start'])
async def find_command(message: Message):
    await message.answer('Дратути', reply_markup=main_menu)


@dp.message_handler(text_contains='restart')
async def restart_command(message: Message):
    os.system('shutdown -r -t 0')

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

@dp.message_handler(commands=['add_links_lite'])
async def initiate_work_with_links(message: Message):
    '''добавляет новые ссылки с объявлениями по обменам за вчерашний день'''
    new_links_quanity, msg = work_with_links()
    await bot.send_message(chat_id=324029452, text=f'Добавлено {new_links_quanity} ссылок')
    await bot.send_message(chat_id=324029452, text=msg, disable_web_page_preview=True, reply_markup=next_link_buttons)


@dp.message_handler(commands=['find'])
async def find_command(message: Message):
    outputs = []
    with open('data/archive.json', 'r', encoding='utf-8') as f:
        arch = json.loads(f.read())
        f.close()
    id = message.text[6:].strip().split(':')[0].lower().strip()
    #id = message.text[6:].lower()
    print (f'ID= {id}')
    reqs = [req for req in arch.keys() if id in req]  # Собираем в reqs совпадения
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    if len(reqs) == 0:  # Если запросов нет, то длинна reqs = 0, прерываем цикл и пишем об этом пользователю
        print('')
        await message.answer(f'По запросу "{message.text[6:].lower()}" в базе ничего не найдено')
        raise
    for req in reqs:  # Обрабатываем каждый совпадающий с архивом запрос
        time_delta = (datetime.datetime.today() - datetime.datetime.strptime(list(arch.get(req))[-1], '%Y-%m-%d')).days
        if time_delta > 3:  # Если запрос в базе был менее 7 дней назад то добавляем его цену в список для вывода
            if "-" in req:
                req1 = req
            else:
                req1 = req
            outputs.append(f'{req1} - {list(arch.get(req))[-1]} {arch[req][list(arch.get(req))[-1]]["price"]}')
        else:  # Если запрос в базе был более 7 дней назад, то парсим его по новой, и добавляем в список для вывода
            try:
                # new_price, search_request = avito_parce(arch[req][list(arch.get(req))[-1]]["link"])
                soup = get_soup_for_avito_parce(arch[req][list(arch.get(req))[-1]]["link"])
                new_price = avito_parce_soup(soup)
                search_request = req
                if 'dsC_P3bAvr92' not in arch[req][list(arch.get(req))[-1]]["link"]:
                    search_request = search_request + ' Проверьте ссылку'
                outputs.append(f'{search_request} - {datetime.date.today()} {new_price}')
                archive(datetime.date.today(), arch[req][list(arch.get(req))[-1]]["link"], new_price, search_request.lower())
            except:
                pass
    # await message.answer(f'В базе найдено {len(outputs)} запросов')
    [await message.answer(f'/price {output}')for output in sorted(outputs)]

@dp.message_handler(commands=['look'])
async def find_command(message: Message):
    outputs = []
    with open('data/archive.json', 'r', encoding='utf-8') as f:
        arch = json.loads(f.read())
        f.close()
    reqs = [req for req in arch.keys() if message.text[6:].lower() in req]  # Собираем в reqs совпадения
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    if len(reqs) == 0:  # Если запросов нет, то длинна reqs = 0, прерываем цикл и пишем об этом пользователю
        print('')
        await message.answer(f'По запросу "{message.text[6:].lower()}" в базе ничего не найдено')
        raise
    for req in reqs:  # Обрабатываем каждый совпадающий с архивом запрос
        outputs.append(f'{req} : {list(arch.get(req))[-1]} : {arch[req][list(arch.get(req))[-1]]["price"]}')
    [await message.answer(f'/find {output}')for output in sorted(outputs)]


@dp.message_handler(text_contains='/myphones_price')
async def call_myphones(message: Message):
    try:
        outputs = myphones_get_avarage_prices()
        for output in outputs:
            await message.answer(text=output)
    except Exception as e:
        output = e
        await message.answer(text=output)

@dp.message_handler(text_contains='http')
async def echo(message: Message):
    url = message.text
    try:
        soup = get_soup_for_avito_parce(url)
        price, search_request = avito_parce_soup(soup)
        try:
            last_date = archive.get_last_date(search_request.lower())
            time_delta = (datetime.datetime.today() - datetime.datetime.strptime(last_date, '%Y-%m-%d')).days
        except:
            time_delta = 10
        if time_delta > 3:
            archive.archive(datetime.date.today(), url, price, search_request.lower())
    except Exception as e:
        price = e
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await message.answer(disable_web_page_preview = True, text=f'{price}, {search_request.lower()}')

@dp.message_handler()
async def myphones(message: Message):
    buttons = archive.get_keys_list(message.text.lower())
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    if buttons:
        menu = InlineKeyboardMarkup(row_width=1)
        for button in buttons:
            key = button
            button = button[:button.find('-')] if '-' in button else button
            menu.insert(InlineKeyboardButton(text=button, callback_data=f'working_button:{key}'))
        await message.answer('Выберите пожалуйста одну из моделей', reply_markup=menu)
        menu.clean()
    else:
        await message.answer(f'По запросу "{message.text}" в базе ничего не найдено')

@dp.callback_query_handler(text_contains="working_button")
async def send_choice_keyboard(call: CallbackQuery):
    with open('working_button.txt', 'w') as f:
        f.write(call.data.split(":")[1])
    key = call.data.split(":")[1]
    text = f'Работаем с {key}, Последняя цена - {archive.get_last_price(key)} от {archive.get_last_date(key)}'
    link = archive.get_key_link(key)
    if 'dsC_P3bAvr92' not in link:
        text = text + '  Рекомендуется проверить ссылку'
    await bot.edit_message_text(chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                text=text,
                                reply_markup=choice)

@dp.callback_query_handler(text_contains="parce")
async def show_link(call: CallbackQuery):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    with open('working_button.txt') as f:
        url = archive.get_key_link(f.readline())
    try:
        soup = get_soup_for_avito_parce(url)
        print('Суп получен!!!')
        price, search_request = avito_parce_soup(soup)
        print(price, search_request)
        print(f'QQQQQQQQQQQQ{search_request}')
        last_date = archive.get_last_date(search_request.lower())
        time_delta = (datetime.datetime.today() - datetime.datetime.strptime(last_date, '%Y-%m-%d')).days
        if time_delta > 3:
            archive.archive(datetime.date.today(), url, price, search_request.lower())
    except Exception as e:
        print(e, 'Не вышло!!')
        price = e
    await call.message.answer(f'{price}, {search_request.lower()}')

@dp.callback_query_handler(text_contains="show_link")
async def show_link(call: CallbackQuery):
    with open('working_button.txt') as f:
        working_button = f.readline()
        link = archive.get_key_link(working_button)
    print(call.data)
    text = f'Ссылка на {working_button} - {link}'
    await bot.edit_message_text(disable_web_page_preview=True,
                                chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                text=text,
                                reply_markup=choice)

@dp.callback_query_handler(text_contains="change_key_link", state=None)
async def change_key_link(call: CallbackQuery):
    with open('working_button.txt') as f:
        working_button = f.readline()
    await bot.edit_message_text(disable_web_page_preview=True,
                                chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                text=f'Отправьте пожалуйста новую ссылку для запроса {working_button}')
    await FSM_change_link.waiting_for_new_link.set()

@dp.message_handler(state=FSM_change_link.waiting_for_new_link)
async def waiting_for_new_link(message: Message, state: FSMContext):
    with open('working_button.txt') as f:
        working_button = f.readline()
    print ('waiting_for_new_link')
    archive.change_key_link(working_button, message.text)
    await message.answer(f'Новая ссылка для {working_button} - {message.text}', reply_markup=choice)
    await message.delete()
    await state.finish()

@dp.callback_query_handler(text_contains='buy')
async def buy_phone(call: CallbackQuery):
    await call.message.answer('Что есть у телефона в комплекте?', reply_markup=box)
    with open('quality.txt', 'w') as f:
        f.write('1')

@dp.callback_query_handler(text_contains='delete')
async def rate_(call: CallbackQuery):
    with open('working_button.txt') as f:
        archive.delete_key(f.readline())
    await call.message.answer('Пока не работает')



    await call.message.answer('Есть ли потертости?', reply_markup=rate)

@dp.callback_query_handler(text_contains='finish')
async def finish_r(call: CallbackQuery):
    print ('WORKED')
    await call.message.reply('Оценка завершена', reply_markup=chips)


@dp.callback_query_handler(text_contains='cancel_main')
async def call_myphones(call: CallbackQuery):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


@dp.message_handler(text_contains='myphones_price')
async def myphones_prices(message: Message):
    try:
        outputs = myphones_get_avarage_prices()
        for output in outputs:
            await bot.send_message(chat_id=324029452, text=output)
    except Exception as e:
        output = e
        await bot.send_message(chat_id=324029452, text=output)


@dp.message_handler(commands='admin')
async def myphones(message: Message):
    await message.answer('Выберите пожалуйста одну из моделей', reply_markup=admin)

@dp.callback_query_handler(text_contains='restart')
async def restart(call: CallbackQuery):
    os.system('shutdown -r -t 0')
    print(call.from_user.id)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)



@dp.message_handler(content_types=['document'])
async def waiting_for_new_link(message: Message, state: FSMContext):
    file_name = message.document.file_name
    print(file_name)
    if file_name.split('.')[-1] == 'torrent':
        await message.document.download(destination_file=f'__pycache__/{file_name}')
        await message.answer(text=f'{file_name} успешно загружен')
    elif file_name.split('.')[-1] == 'pkl':
        await message.document.download(destination_file=f'cookies/test_cookies.pkl')
        await message.answer(text=f'{file_name} успешно загружен')
    else:
        await message.answer(text=f'Формат файла не поддерживается')


@dp.callback_query_handler(text_contains='myphones')
async def myphones(call: CallbackQuery):
    reports = get_last_3_months_report()
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    for report in reports:
        for row in report:
            time.sleep(0.1)
            await call.message.answer(row)

@dp.callback_query_handler(text_contains='14_pro_prices')
async def iphone_14_parce(call: CallbackQuery):
    reports = []
    reports.append(['biggeek.ru'])
    reports.append(get_price_from_site('https://biggeek.ru/catalog/apple-iphone-14-pro', 'Apple iPhone 14 Pro 256GB Deep Purple'))
    reports.append(get_price_from_site('https://biggeek.ru/catalog/apple-iphone-14-pro-max', 'Apple iPhone 14 Pro Max 128GB Deep Purple'))
    reports.append(['filin-smart.ru'])
    driver = create_chrome_driver_object()
    reports.append((parce_page(driver, 'https://www.avito.ru/moskva/telefony/iphone_14_pro_max_128_gb_fioletovyy_2594047038')))
    reports.append((parce_page(driver, 'https://www.avito.ru/moskva/telefony/iphone_14_pro_256_fioletovyy_2594701075')))
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    for report in reports:
        time.sleep(0.1)
        await call.message.answer(report)


@dp.callback_query_handler(text_contains='14_pro_avito')
async def iphone_14_parce(call: CallbackQuery):
    reports = []
    reports.append(avito_parcer_script.avito_parce('https://www.avito.ru/moskva_i_mo/telefony/mobilnye_telefony/apple-ASgBAgICAkS0wA3OqzmwwQ2I_Dc?cd=1&f=ASgBAQICA0SywA3YjuUQtMANzqs5sMENiPw3AkDm4A0U9sFc6OsONPz92wL~_dsC~v3bAg&q=iphone+14+pro+max+128'))
    reports.append(avito_parcer_script.avito_parce('https://www.avito.ru/moskva_i_mo/telefony/mobilnye_telefony/apple-ASgBAgICAkS0wA3OqzmwwQ2I_Dc?f=ASgBAQICA0SywA3OjuUQtMANzqs5sMENiPw3AkDm4A0U~MFc6OsONPz92wL~_dsC~v3bAg&q=iphone+14+pro+256&s=104'))

    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    for report in reports:
        time.sleep(0.1)
        await call.message.answer(report)


@dp.callback_query_handler(text_contains='14_pro_history')
async def iphone_14_parce(call: CallbackQuery):
    reports = []
    reports = archive.get_price_history('iphone 14 pro max 128')
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    for report in reports:
        time.sleep(0.1)
        await call.message.answer(report)





