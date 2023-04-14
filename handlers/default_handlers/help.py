from telebot.types import Message
from config_data.config import COMMANDS_FOR_HELP_HANDLER
from loader import bot

@bot.message_handler(commands=["help"])
def bot_help(message: Message):

    text = [f"/{command} - {desk}" for command, desk in COMMANDS_FOR_HELP_HANDLER]
    bot.send_message(message.chat.id, "Команды: ")

    bot.send_message(message.chat.id, "\n".join(text))

