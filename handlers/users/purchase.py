import datetime
import json
import os

import time
import types
from multiprocessing import Pool
import threading
from my_libs.mycars_lib import daily_mean
current_directory = os.getcwd()
print(f"Текущая директория: {current_directory}")
from my_libs.cian.parce_many_links import parce_many_links, get_link_list_from_url

import avito_parcer_script
from my_libs.big_geek_parce import get_price_from_site
from my_libs.cian.parce_cian import cian_parce_2

from my_libs.cian.parce_many_links import cian_get_links_from_report
from add_links_lite import work_with_links

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import Message, CallbackQuery
from aiogram import types

from my_libs.mycars_lib import daily_mean
from my_libs.myphones_lib import get_last_3_months_report
import archive
from avito_parcer_script import myphones_get_avarage_prices, get_soup_for_avito_parce, avito_parce_soup, avito_auto_parce_soup
from keyboards.inline.choice_buttons import choice, admin, cancel_button, next_link_buttons, main_menu
from keyboards.inline.equipment import box, charger, check, scratches, chips
from loader import dp, bot
from my_libs.libs_selenium import create_chrome_driver_object
import asyncio
from configparser import ConfigParser
from telethon import TelegramClient

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
    await message.answer('/cars - команды по автомобилям\n'
                         '/phones - команды по телефонам', reply_markup=main_menu)

@dp.message_handler(commands=['cars'])
async def cars_command(message: Message):
    await message.answer('/cars_daily_mean - ежедневный отчет\n'
                         '/cars_full_report - исходный файл\n'
                         '/mycars - запрос средних цен')

@dp.message_handler(commands=['phones'])
async def phones_command(message: Message):
    await message.answer('/archive_status - сколько устаревших объявлений\n'
                         '/archive_update - обновить архив\n'
                         '/myphones - стоимость телефонов на руках')

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

@dp.message_handler(text_contains='/myphones2')
async def call_myphones(message: Message):
    try:
        outputs = myphones_get_avarage_prices(range_="myphones2")
        for output in outputs:
            await message.answer(text=output)
    except Exception as e:
        output = e
        await message.answer(text=output)

@dp.message_handler(text_contains='/myphones')
async def call_myphones(message: Message):
    try:
        outputs = myphones_get_avarage_prices()
        for output in outputs:
            await message.answer(text=output)
    except Exception as e:
        output = e
        await message.answer(text=output)

@dp.message_handler(text_contains='/mycars')
async def call_myphones(message: Message):
    try:
        outputs = avito_parcer_script.myphones_get_avarage_prices(range_="mycars")
        for output in outputs:
            await message.answer(text=output)
    except Exception as e:
        output = e
        await message.answer(text=output)

@dp.message_handler(text_contains='archive_status')
async def call_myphones(message: Message):
    output = archive.archive_status()
    await message.answer(text=output)
@dp.message_handler(text_contains='archive_update')
async def call_myphones(message: Message):
    avito_parcer_script.update_archive(30)
    await message.answer(text='Обновлено 30 объявлений')

@dp.message_handler(text_contains='avtomobili')
async def echo(message: Message):
    url = message.text
    try:
        soup = get_soup_for_avito_parce(url)
        price, search_request = avito_auto_parce_soup(soup)
        price_std, search_request = avito_parce_soup(soup)
        # try:
        #     last_date = archive.get_last_date(search_request.lower())
        #     time_delta = (datetime.datetime.today() - datetime.datetime.strptime(last_date, '%Y-%m-%d')).days
        # except:
        #     time_delta = 10
        # if time_delta > 3:
        archive.archive(datetime.date.today(), url, price, search_request.lower())
        print ('ПроХОДИИИИИИИТ!!!!!!!!')
    except Exception as e:
        price = e
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await message.answer(disable_web_page_preview = True, text=f'{price}, {price_std}, {search_request.lower()}')

@dp.message_handler(text_contains='avito')
async def echo(message: Message):
    url = message.text
    try:
        driver = create_chrome_driver_object()
        soup = get_soup_for_avito_parce(url, driver, attempts=5 )
        price, search_request = avito_parce_soup(soup)
        # try:
        #     last_date = archive.get_last_date(search_request.lower())
        #     time_delta = (datetime.datetime.today() - datetime.datetime.strptime(last_date, '%Y-%m-%d')).days
        # except:
        #     time_delta = 10
        # if time_delta > 3:
        archive.archive(datetime.date.today(), url, price, search_request.lower())
    except Exception as e:
        price = e
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await message.answer(disable_web_page_preview = True, text=f'{price}, {search_request.lower()}')

@dp.message_handler(text_contains='cian')
async def echo(message: Message):
    url = message.text
    outputs = []
    try:

        average_flat_price, average_flat_price_nearby, flat_price = cian_parce_2(url)
        outputs.append(f'{flat_price} - Цена квартиры')

        outputs.append(f'{average_flat_price}({round((flat_price+50)/average_flat_price, 2)}) - средняя цена по дому')
        outputs.append(f'{average_flat_price_nearby}({round((flat_price+50)/average_flat_price_nearby, 2)}) - средняя цена в округе')
        outputs.append(f'{round( ((flat_price+50)/average_flat_price_nearby + (flat_price+50)/average_flat_price)/2,2)} - общая оценка')
    except Exception as e:
        outputs.append(e)
    # await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    for output in outputs:
        await bot.send_message(chat_id=message.chat.id, text=output)

@dp.message_handler(text_contains='flipping')
async def echo(message: Message):
    url = message.text
    outputs = []
    try:
        link_list = get_link_list_from_url()
        outputs = parce_many_links(link_list=link_list)
    except Exception as e:
        outputs.append(e)

    for output in outputs:
        await bot.send_message(chat_id=message.chat.id, text=output)

@dp.message_handler(commands='cars_daily_mean')
async def cars_daily_mean(message: Message):
    daily_mean()
    await message.answer_document(open('data/mycars/mycarsreport.csv', 'rb'))

@dp.message_handler(commands='cars_full_report')
async def cars_daily_mean(message: Message):
    await message.answer_document(open('data/mycars/mycars2.xlsx', 'rb'))

@dp.message_handler(commands='currency')
async def send_currency(message: types.Message):
    # Выводим текущую директорию
    import os
    current_directory = os.getcwd()
    print(f"Текущая директория: {current_directory}")

    # Читаем последние 5 строк из файла
    try:
        with open('my_libs/currency/data/currency.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
            last_five_lines = lines[-5:]  # Получаем последние 5 строчек

            # Форматируем строки в читаемый вид
            formatted_lines = []
            for line in last_five_lines:
                date, bot_rate, cbr_rate, difference = line.strip().split(',')
                formatted_lines.append(
                    f"Дата: {date}\nКурс (БОТ): {bot_rate} руб.\nКурс (ЦБ РФ): {cbr_rate} руб.\nРазница: {difference} руб.\n"
                )
            response = '\n'.join(formatted_lines)
    except FileNotFoundError:
        response = "Файл не найден. Проверьте путь к файлу."
    except Exception as e:
        response = f"Произошла ошибка: {e}"

    # Удаляем сообщение пользователя
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

    # Отправляем ответ с форматированными данными
    await message.answer(response)
@dp.message_handler(lambda message: not message.text.startswith('/'))
async def myphones(message: Message):
    buttons = archive.get_keys_list(message.text.lower())
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    if buttons:
        buttons.sort()

        menu = InlineKeyboardMarkup(row_width=1)
        for button in buttons:
            key = button
            button = button[:button.find('-')] if '-' in button else button
            menu.insert(InlineKeyboardButton(text=button, callback_data=f'w_b:{key}'))
        await message.answer('Выберите пожалуйста одну из моделей', reply_markup=menu)
        menu.clean()
    else:
        await message.answer(f'По запросу "{message.text}" в базе ничего не найдено')

@dp.message_handler(commands=['currency'])
async def send_currency(message: types.Message):
    # Читаем последние 5 строк из файла
    try:
        with open('my_libs/currency/data/currency.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
            last_five_lines = lines[-5:]  # Получаем последние 5 строчек
            response = '\n'.join([line.strip() for line in last_five_lines])
    except FileNotFoundError:
        response = "Файл не найден. Проверьте путь к файлу."
    except Exception as e:
        response = f"Произошла ошибка: {e}"

    # Удаляем сообщение пользователя
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

    # Отправляем ответ с последними строками файла
    await message.answer(response)


@dp.message_handler(commands=['currency_add'])
async def add_currency_chat(message: types.Message):
    """Add new Telegram channel to currency parser list."""
    channel = message.get_args()
    if not channel:
        await message.answer('Укажите канал после команды, например /currency_add @channel')
        return
    if not channel.startswith('@'):
        channel = '@' + channel

    config = ConfigParser()
    config.read('my_libs/currency/config.ini')
    api_id = config.getint('telegram', 'api_id')
    api_hash = config.get('telegram', 'api_hash')
    session_name = config.get('telegram', 'session_name')

    async with TelegramClient(session_name, api_id, api_hash) as tg_client:
        try:
            entity = await tg_client.get_entity(channel)
        except Exception as e:
            await message.answer(f'Не удалось получить данные канала: {e}')
            return
        chat_id = entity.id
        chat_name = entity.title

    chats_file = 'my_libs/currency/data/chats.txt'
    try:
        with open(chats_file, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        lines = []

    existing_ids = {line.split(' - ')[0] for line in lines}
    if str(chat_id) in existing_ids:
        await message.answer('Канал уже есть в списке.')
        return

    with open(chats_file, 'a', encoding='utf-8') as f:
        f.write(f'{chat_id} - {chat_name}\n')

    await message.answer(f'Канал {chat_name} добавлен в список.')

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
@dp.callback_query_handler(text_contains="w_b")
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
        price, search_request = avito_parce_soup(soup)
        # last_date = archive.get_last_date(search_request.lower())
        # time_delta = (datetime.datetime.today() - datetime.datetime.strptime(last_date, '%Y-%m-%d')).days
        # if time_delta > 3:
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
    await call.message.answer('Запись удалена')



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
    elif file_name.split('.')[-1] == 'xlsx':
        await message.document.download(destination_file=f'my_libs/cian/offers.xlsx')
        await message.answer(text=f'{file_name} успешно загружен')
        links = cian_get_links_from_report()
        outputs = parce_many_links(link_list=links)
        for output in outputs:
            await message.answer(text=output)
    else:
        await message.answer(text=f'Формат файла не поддерживается')


@dp.callback_query_handler(text_contains='myphones')
async def myphones(call: CallbackQuery):
    print("MYPHONES PARCE")
    reports = myphones_get_avarage_prices()
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    for report in reports:
        time.sleep(0.1)
        await call.message.answer(report)

@dp.callback_query_handler(text_contains='price_history')
async def price_history(call: CallbackQuery):

    with open('working_button.txt') as f:
        key = f.readline()
    reports = []
    reports = archive.get_price_history(key)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    for report in reports:
        time.sleep(0.1)
        await call.message.answer(report)

@dp.callback_query_handler(text_contains='add_links')
async def add_links(call: CallbackQuery):
    '''добавляет новые ссылки с объявлениями по обменам за вчерашний день'''
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    new_links_quanity, msg = work_with_links()
    await bot.send_message(chat_id=324029452, text=f'Добавлено {new_links_quanity} ссылок')
    await bot.send_message(chat_id=324029452, text=msg, disable_web_page_preview=True, reply_markup=next_link_buttons)










