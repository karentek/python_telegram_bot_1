from datetime import date
from loader import bot
from telebot.types import Message
from utils.surch.hotels_by_city import LocationID
from utils.surch.hotels_list import HotelsID
from database.common.models import Flag
from utils.surch.deteil_hotel_info import deteil_info
from states.high_low_func import HighLowFunc
from loguru import logger


@bot.message_handler(commands=["lowest_price"])
def choose_hotel_h(message: Message) -> None:
    bot.send_message(message.from_user.id, f''
                                           f'{message.from_user.username}, '
                                           f'Введите название страны')
    bot.set_state(message.from_user.id, HighLowFunc.country_l, message.chat.id)


@bot.message_handler(state=[HighLowFunc.country_l])
def get_country_h(message: Message) -> None:
    """
    :get_country_: обработчик сообщений ожидает от пользователя наименованием страны.
                  Проверяется правильность ввода, а именно:
                  сообщение должно состоять только из букв.
                  Если условие не выполняется, блок сценария повторяется.
                  Предлагается ввести наименование города для выполнения
                  следующего блока сценария.

    :param message: объект pyTelegramBotApi
    :return: None
    """
    logger.info("Введено название страны")
    if message.text.isalpha():
        bot.send_message(message.from_user.id, 'Спасибо записал. Теперь введи город,'
                                               ', и я выведу самый дешевый отель в нем')
        bot.set_state(message.from_user.id, HighLowFunc.city_l, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data_h:
            data_h['country'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Можно вводить только буквы, повтори еще раз')


@bot.message_handler(state=[HighLowFunc.city_l])
def get_city_h(message: Message) -> None:
    """
    :get_country_: обработчик ожидает от пользователя сообщение с наименованием города.
                  Проверяется правильность ввода, а именно:
                  сообщение должно состоять только из букв.
                  Если условие не выполняется, блок сценария повторяется.
                  В случае успешной проверки
                  производится попытка совершить API запрос, обработать полученный JSON,
                  и извлечь ID искомого города, в случае неудачной попытки вызывается ошибка,
                  после чего предлагается начать заново ввод данных.
                  Далее предлагается ввести новое сообщение и вызывается
                  обработчик для выполнения следующего блока сценария

    :param message:
    :return:
    """
    logger.info("Введено название города")
    if message.text.isalpha():
        try:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data_h:
                data_h['city'] = message.text
                create_json_with_location_id = LocationID.set_city()
                create_json_with_location_id(data_h['city'], data_h['country'])
                get_location_id = LocationID.get_id()
                id = get_location_id()
                if not id:
                    raise Exception
                data_h['city_id'] = id
                print(data_h['city_id'])
                print('проверка функции в гет сити аш', data_h['city_id'][0])
            get_hotels_list_h(message)
        except Exception:
            bot.send_message(message.from_user.id, 'Произошла ошибка, видимо такой локации не существует\n'
                                                   'Попробуйте заново\n'
                                                   'Введите город')
            bot.set_state(message.from_user.id, HighLowFunc.city_l, message.chat.id)

    else:
        bot.send_message(message.from_user.id, 'Можно вводить только буквы, повтори еще раз')


def get_hotels_list_h(message: Message) -> None:
    """
    :get_hotels_list: функция, на вход подается сообщение
                  со всеми введенными данными.
                  И выполняется попытка произвести API запрос
                  с поиском отелей по заданным диапазонам и условиям.
                  При неудачной попытке запроса предлагается начать снова, но не сначала,
                   а с ввода диапазона цен.

                  В случае успеха формируется список с найденными отелями и отправляется пользователю

    :param
        message: объект pyTelegramBotApi
        msg (str): необходим для записи в поле БД в одну строку

    :return: None
    """

    logger.info("Отправляются собранные данные для выполнения запроса API")
    try:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data_h:
            date_in = {
                "day": date.today().day,
                "month": date.today().month,
                "year": date.today().year}
            date_out = {
                "day": date.today().day + 7,
                "month": date.today().month,
                "year": date.today().year}
            create_json_with_hotels_propertys = HotelsID.set_propertys()
            create_json_with_hotels_propertys(
                data_h['city_id'][0],
                date_in=date_in,
                date_out=date_out,
                guests=[
                    {
                        "adults": 2,
                        "children":
                            [
                                {"age": 5}, {"age": 7}
                            ]
                    }
                ],
                min_price=1,
                max_price=100000)

            hotels_list = HotelsID.get_hotels_list()
            hotels_list = hotels_list()

            print('ID города {}. название {}'.format(data_h['city_id'][0], data_h['city_id'][1]))
        country_code = data_h['city_id'][2]
        logger.info("Ищем смайлик флаг в БД")
        retrieved = Flag.select().where(Flag.country_name == country_code).get()

        if retrieved:
            flag = retrieved.iso_code
        else:
            flag = '***'
        logger.info("Отправляем сообщения пользователю")

        info = deteil_info(hotels_list[0][0])
        hotel = hotels_list[0]
        bot.send_message(message.from_user.id, f'{flag} {flag} {flag} {flag} {flag} {flag}\n'
                                               f'{hotel[1]} - '
                                               f'${hotel[2]}\n'
                                               f'До центра города - {hotel[3]} км.\n'
                                               f'Адрес отеля {info[0]}\n')
        for i_photo in range(0, 7):
            bot.send_message(message.from_user.id, f'{info[2][i_photo]}\n')

        bot.send_message(message.from_user.id, f'Для дальнейшей работы выберите пункт меню')
        bot.delete_state(message.from_user.id, message.chat.id)

    except TypeError:
        bot.send_message(message.from_user.id,
                         f'Что то пошло не так, попробуйте сделать запрос снова\n')
        bot.set_state(message.from_user.id, HighLowFunc.city_l, message.chat.id)
