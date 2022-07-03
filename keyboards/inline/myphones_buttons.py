from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_datas import buy_callback, sell_callback

myphones_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Myphones", callback_data='myphones'),
            InlineKeyboardButton(text="Продать", callback_data='sell'),
            InlineKeyboardButton(text="Оценить", callback_data='rate')
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="cancel")
        ]
    ]
)