from telebot.types import Message
from python_basic_diploma.loader import bot

from python_basic_diploma.database.common.models import db, History
from python_basic_diploma.database.core import crud

db_read = crud.retrieve()


@bot.message_handler(commands=["history"])
def choose_hotel(message: Message) -> None:
    retrieved = db_read(db, History, History.user_request, History.bot_response)

    for element in retrieved:
        bot.send_message(message.from_user.id, f'{element.user_request}\n{element.bot_response}')
