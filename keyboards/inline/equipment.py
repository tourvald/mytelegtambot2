from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

box = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Коробка",
                                 callback_data='charger:yes'
                                 ),
            InlineKeyboardButton(text="Без коробки",
                                 callback_data='charger:no'
                                 )
        ]]
)

charger = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Есть зарядка",
                                 callback_data='cheсk:yes'
                                 ),
            InlineKeyboardButton(text="Нет зарядки",
                                 callback_data='cheсk:no'
                                 )
        ]]

)

check = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Есть чек",
                                 callback_data='scratches:yes'
                                 ),
            InlineKeyboardButton(text="Нет чека",
                                 callback_data='scratches:no'
                                 )
        ]]

)

scratches = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Есть царапины",
                                 callback_data='chips:yes'
                                 ),
            InlineKeyboardButton(text="Нет царапин",
                                 callback_data='chips:no'
                                 )
        ]]

)

chips = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Есть сколы",
                                 callback_data='scuffs:yes'
                                 ),
            InlineKeyboardButton(text="Нет нет сколов",
                                 callback_data='scuffs:no'
                                 )
        ]]

)



scuffs = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Есть царапины",
                                 callback_data='scuffs:yes'
                                 ),
            InlineKeyboardButton(text="Нет царапин",
                                 callback_data='scuffs:no'
                                 )
        ]]

)
