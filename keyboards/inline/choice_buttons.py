from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_datas import buy_callback, sell_callback


next_link_buttons = InlineKeyboardMarkup(
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
            InlineKeyboardButton(text="restart", callback_data='restart')
        ]
    ]
)

main_menu = choice = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Myphones", callback_data='myphones'),
            InlineKeyboardButton(text="Add Links", callback_data='add_links')
        ],

        [
            InlineKeyboardButton(text="Отмена", callback_data="cancel_main")
        ]
    ]
)


choice = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Удалить", callback_data='delete'),
            InlineKeyboardButton(text="История цен", callback_data='price_history')

        ],
        [
            InlineKeyboardButton(text="Ссылка", callback_data='show_link'),
            InlineKeyboardButton(text="Изм. Ссылку", callback_data='change_key_link'),
            InlineKeyboardButton(text="Парсинг", callback_data='parce')
        ],
        [
            InlineKeyboardButton(text="Отмена", callback_data="cancel_main")
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