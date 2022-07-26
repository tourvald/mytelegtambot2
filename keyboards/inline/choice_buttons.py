from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_datas import buy_callback, sell_callback

cancel_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Отмена', callback_data='cancel')
        ]
    ]
)

admin = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="torrent", callback_data='torrent'),
            InlineKeyboardButton(text="restart", callback_data='restart')
        ]
    ]
)

choice = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Купить", callback_data=buy_callback.new(
                item="iphone 12 pro max 128", price="99000"
            )),
            InlineKeyboardButton(text="Myphones", callback_data='myphones'),
            InlineKeyboardButton(text="Оценить", callback_data='rate')
        ],
        [
            InlineKeyboardButton(text="Ссылка", callback_data='show_link'),
            InlineKeyboardButton(text="Изм. Ссылку", callback_data='change_key_link'),
            InlineKeyboardButton(text="Парсинг", callback_data='parce')
        ],
        [
            InlineKeyboardButton(text="Отмена", callback_data="cancel")
        ]
    ]
)

quality = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Идеал', callback_data=buy_callback.new(
                item="iphone 12 pro max", price="93000"
            )),
            InlineKeyboardButton(text='Потертости', callback_data=buy_callback.new(
                item="iphone 12 pro max", price="93000"
            ))
        ]
    ]
)