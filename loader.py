from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import config
import logging
from aiogram.contrib.fsm_storage.memory import MemoryStorage
storage = MemoryStorage()
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)
logging.basicConfig()