from telebot.types import Message
from loader import bot
from database.common.models import History


@bot.message_handler(commands=["history"])
def choose_hotel(message: Message) -> None:
    """
    :choose_hotel: обработчик запускается командой "history"
                   выводит последние 10 запросов пользователя.
                   В случае если сообщение содержащее список найденных отелей
                   превыси 4096 символов сообщение не отправится, так как это
                   максимально допустимое количество символов сообщения Telegram

    """
    retrieved = History.select().where(History.chat_id == message.chat.id)

    if len(retrieved) == 0:
        bot.send_message(message.from_user.id, f'В истории нет сохраненных записей\n')
    else:

        if len(retrieved) > 10:
            for index, element in enumerate(retrieved):
                if index >= len(retrieved) - 10:
                    if len(element.bot_response) < 4096:
                        bot.send_message(message.from_user.id, f'{element.user_request}\n')
                        bot.send_message(message.from_user.id, f'{element.bot_response}')
                    else:
                        bot.send_message(message.from_user.id, f'{element.user_request}\n'
                                                               f'______________________'
                                                               f'Ответ бота для данного запроса '
                                                               f'превышает допустимое число символов. '
                                                               f'Сузьте диапазон этого запроса чтобы '
                                                               f'можно было корректно вывести список '
                                                               f'отелей на экран')
        elif len(retrieved) == 10:
            bot.send_message(message.from_user.id, f'Пока не было ни одного запроса\n')
        else:
            for element in retrieved:
                if len(element.bot_response) < 4096:
                    bot.send_message(message.from_user.id, f'{element.user_request}\n')
                    bot.send_message(message.from_user.id, f'{element.bot_response}')
                else:
                    bot.send_message(message.from_user.id, f'{element.user_request}\n'
                                                           f'______________________'
                                                           f'Ответ бота для данного запроса '
                                                           f'превышает допустимое число символов. '
                                                           f'Сузьте диапазон этого запроса чтобы '
                                                           f'можно было корректно вывести список '
                                                           f'отелей на экран')

