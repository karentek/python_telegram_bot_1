from telebot import TeleBot
from telebot.storage import StateMemoryStorage
from python_basic_diploma.config_data import config

storage = StateMemoryStorage()
bot = TeleBot(token=config.BOT_TOKEN, state_storage=storage)
