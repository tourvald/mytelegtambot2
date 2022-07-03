from aiogram.utils.callback_data import CallbackData

buy_callback = CallbackData("buy", "item", "price")
sell_callback = CallbackData("sell", "item", "price")
rate_callback = CallbackData("sell", "item", "price")