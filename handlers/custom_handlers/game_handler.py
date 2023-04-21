import random
from loader import bot
from telebot.types import Message
from database.common.models import Flag
from states.game import Game
from loguru import logger


@bot.message_handler(commands=["game"])
def start_game(message: Message) -> None:
    logger.info("Начали игру")
    random_flag_func(message)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as game_data:
        logger.info("Обнулили результаты")

        game_data['Угадал'] = 0
        game_data['Ошибся'] = 0


def random_flag_func(message: Message) -> None:
    """
    :random_flag_func: функция которая рандомно выбирает и выдает флаг страны
                        на экран, при этом записываются данные в файл game_data
                        для последующей обработки

    """
    logger.info("Выводим флаг")
    random_index = random.randint(1, 258)
    random_flag = Flag.select().where(Flag.id == random_index - 1).get()
    bot.send_message(message.from_user.id, f'{random_flag.iso_code}')
    bot.send_message(message.from_user.id, 'Какой стране принадлежит этот флаг?\n'
                                           'Для остановки введите "стоп"')
    bot.set_state(message.from_user.id, Game.check_country, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as game_data:
        logger.info("Записываем данные в game_data")
        game_data['iso_code'] = random_flag.iso_code
        game_data['country_name'] = random_flag.country_name
        game_data['russian_name'] = random_flag.russian_name



@bot.message_handler(state=[Game.check_country])
def check_country(message: Message) -> None:
    """
    :get_country_: обработчик ожидает от пользователя сообщение с наименованием страны.
                  Сообщение сверяется с полем БД соответствующем флагу
                  И выводится на экран результат
    :param message:
    :return:
    """
    logger.info("Проверяем название страны на соответствие флагу")
    with bot.retrieve_data(message.from_user.id, message.chat.id) as game_data:
        pass

    if game_data['country_name'].lower() == message.text.lower() or\
       game_data['russian_name'].lower() == message.text.lower():
        game_data['Угадал'] += 1
        bot.send_message(message.from_user.id, 'Верно')
        random_flag_func(message)
    elif message.text.lower() == 'стоп':
        logger.info("Выводим результаты")

        bot.send_message(message.from_user.id,
                         f'Результаты игры\n'
                         f'Угадал {game_data["Угадал"]} раз\n'
                         f'Ошибся {game_data["Ошибся"]} раз\n'
                         f'Для дальнейшей работы выберите пункт меню')
        bot.delete_state(message.from_user.id, message.chat.id)
    else:
        bot.send_message(message.from_user.id,
                         f'Все говорят {message.text}, а это {game_data["russian_name"]}')
        game_data['Ошибся'] += 1
        random_flag_func(message)




