import logging
import archive
from avito_parcer_script import myphones_get_avarage_prices, get_soup_for_avito_parce, avito_parce_soup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from avito_parcer_script import avito_parce
from keyboards.inline.choice_buttons import choice
from keyboards.inline.equipment import box, charger, check, scratches, chips, scuffs
from loader import dp, bot
import datetime
import json


ti = 0
data = {}
class FSM_change_link(StatesGroup):
    waiting_for_new_link = State()

class FSM_buy_phone(StatesGroup):
    equipment = State()

@dp.message_handler(commands=['start'])
async def find_command(message: Message):
    await message.answer('Дратути')

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
        if time_delta > 0:  # Если запрос в базе был менее 7 дней назад то добавляем его цену в список для вывода
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

@dp.message_handler(text_contains='http')
async def echo(message: Message):
    url = message.text
    try:
        soup = get_soup_for_avito_parce(url)
        price = avito_parce_soup(soup)
    except Exception as e:
        price = e
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await message.answer(disable_web_page_preview = True, text=price)

@dp.message_handler(commands='work')
async def myphones(message: Message):
    buttons = archive.get_keys_list(message.text.lower()[6:])
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
        price = avito_parce_soup(soup)
    except Exception as e:
        price = e
    await call.message.answer(price)

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

def change_quality(amount):
    with open('quality.txt') as f:
        quality = f.readline()
    quality = round((float(quality) - amount),2)
    with open('quality.txt', 'w') as f:
        f.write(str(quality))
    print(quality)


@dp.callback_query_handler(text_contains='charger')
async def charger_(call: CallbackQuery):
    if call.data.split(':')[1] == 'no':
        change_quality(0.04)
    await call.message.answer('Есть ли родная зарядка?', reply_markup=charger)

@dp.callback_query_handler(text_contains='cheсk')
async def check_(call: CallbackQuery):
    if call.data.split(':')[1] == 'no':
        change_quality(0.04)
    await call.message.answer('Есть ли чек?', reply_markup=check)

@dp.callback_query_handler(text_contains='scratches')
async def scratches_(call: CallbackQuery):
    if call.data.split(':')[1] == 'no':
        change_quality(0.04)
        print('нет чека')
    await call.message.answer('Есть ли царапины?', reply_markup=scratches)

@dp.callback_query_handler(text_contains='chips')
async def chips_(call: CallbackQuery):
    if call.data.split(':')[1] == 'yes':
        print ('есть царапины')
        change_quality(0.04)
    await call.message.answer('Есть ли сколы?', reply_markup=chips)

@dp.callback_query_handler(text_contains='chips')
async def scuffs_(call: CallbackQuery):
    if call.data.split(':')[1] == 'yes':
        change_quality(0.03)
        print('Есть потертости')
    await call.message.answer('Есть ли потертости?', reply_markup=scuffs)



@dp.callback_query_handler(text_contains='rate')
async def rate_(call: CallbackQuery):
    global ti
    ti += 1
    print(ti)
    rate = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Нет",
                                 callback_data='rate'
                                 ),
            InlineKeyboardButton(text="Да",
                                 callback_data='finish'
                                 )
        ]]
    )



    await call.message.answer('Есть ли потертости?', reply_markup=rate)

@dp.callback_query_handler(text_contains='finish')
async def finish_r(call: CallbackQuery):
    print ('WORKED')
    await call.message.reply('Оценка завершена', reply_markup=chips)


@dp.message_handler(text_contains='myphones_price')
async def myphones_prices(message: Message):
    try:
        outputs = myphones_get_avarage_prices()
        for output in outputs:
            await message.answer(output)
    except Exception as e:
        output = e
        await message.answer(output)





