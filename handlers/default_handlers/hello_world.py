from telebot.types import Message
from python_basic_diploma.config_data.config import DEFAULT_COMMANDS
from python_basic_diploma.loader import bot


@bot.message_handler(commands=["hello_world"])
def bot_start(message: Message):
    bot.reply_to(message, f"/hello_world! Мир привет!!!")
