from python_basic_diploma.loader import bot
from telebot.types import Message
from python_basic_diploma.utils.surch.hotels_by_city import LocationID
from python_basic_diploma.utils.surch.hotels_list import HotelsID
from python_basic_diploma.utils.check_date import Date
from python_basic_diploma.database.common.models import db, History
from python_basic_diploma.database.core import crud
from python_basic_diploma.utils.surch.deteil_hotel_info import deteil_info
from python_basic_diploma.states.hotel_information import HotelInfoState


db_write = crud.create()

@bot.message_handler(commands=["choose_a_hotel"])
def choose_hotel(message: Message) -> None:

    """
    Сценарий обработчиков сообщений запускается командой choose_a_hotel
    в данном блоке пользователю предлагается ввести название страны для последующей обработки в
    следующем шаге сценария

    :param message: объект pyTelegramBotApi
    :return: None
    """

    bot.set_state(message.from_user.id, HotelInfoState.country, message.chat.id)
    bot.send_message(message.from_user.id, f'{message.from_user.username}, введи страну для поиска отеля')

@bot.message_handler(state=[HotelInfoState.country])
def get_country_(message: Message) -> None:

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

    if message.text.isalpha():
        bot.send_message(message.from_user.id, 'Спасибо записал. Теперь введи город')
        bot.set_state(message.from_user.id, HotelInfoState.city, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['country'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Можно вводить только буквы, повтори еще раз')

@bot.message_handler(state=[HotelInfoState.city])
def get_city_(message: Message) -> None:
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
    if message.text.isalpha():
        try:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['city'] = message.text
                create_json_with_location_id = LocationID.set_city()
                create_json_with_location_id(data['city'], data['country'])
                get_location_id = LocationID.get_id()
                id = get_location_id()
                if not id:
                    raise Exception
                data['city_id'] = id
            bot.send_message(message.from_user.id, 'Спасибо записал. Теперь введи минимальную стоимость')
            bot.set_state(message.from_user.id, HotelInfoState.min_price, message.chat.id)
        except Exception:
            bot.send_message(message.from_user.id, 'Произошла ошибка, видимо такой локации не существует\n'
                                                   'Попробуйте заново\n'
                                                   'Введите страну поиска')
            bot.set_state(message.from_user.id, HotelInfoState.country, message.chat.id)

    else:
        bot.send_message(message.from_user.id, 'Можно вводить только буквы, повтори еще раз')

@bot.message_handler(state=[HotelInfoState.min_price])
def get_min_price(message: Message) -> None:
    """
    :get_min_price: обработчик ожидает сообщение
                  с минимальной приемлемой для пользователя стоимостью
                  проверяется правильность ввода, а именно:
                  сообщение должно состоять только из цифр.
                  Если условие не выполняется, блок сценария повторяется. В противном случае
                  предлагается ввести новое сообщение и вызывается
                  функция для выполнения следующего блока сценария

    :param message: объект pyTelegramBotApi
    :return: None
    """

    if message.text.isdigit():
        bot.send_message(message.from_user.id, 'Спасибо записал. Теперь введи максимальную стоимость')
        bot.set_state(message.from_user.id, HotelInfoState.max_price, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['min_price'] = int(message.text)
    else:
        bot.send_message(message.from_user.id, 'Цена может быть только числом, попробуйте ввести еще раз')

@bot.message_handler(state=[HotelInfoState.max_price])
def get_max_price(message: Message) -> None:

    """
    :get_max_price: обработчик ожидает сообщение
                  с максимальной приемлемой для пользователя стоимостью
                  проверяется правильность ввода, а именно:
                  сообщение должно состоять только из цифр.
                  Если условие не выполняется, блок сценария повторяется. В противном случае
                  предлагается ввести новое сообщение и вызывается
                  функция для выполнения следующего блока сценария

    :param message: объект pyTelegramBotApi
    :return: None
    """

    if message.text.isdigit():
        bot.send_message(message.from_user.id, 'Спасибо записал. Теперь введи дату заселения\n'
                                               'Правильный формат: dd.mm.yyyy\n')
        bot.set_state(message.from_user.id, HotelInfoState.date_chack_in, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['max_price'] = int(message.text)
    else:
        bot.send_message(message.from_user.id, 'Цена может быть только числом, попробуйте ввести еще раз')

@bot.message_handler(state=[HotelInfoState.date_chack_in])
def get_check_in_date(message: Message) -> None:

    """
    :get_check_in_date: обработчик ожидает сообщение
                  с датой заселения.
                  Проверяется корректность ввода даты, с помощью методов класса Date
                  Если дата была введена не корректно, блок сценария повторяется.
                  После чего предлагается ввести новое сообщение и вызывается
                  обработчик для выполнения следующего блока сценария

    :param message: объект pyTelegramBotApi
    :return: None
    """

    try:
        date = Date.from_string(message.text)
        if Date.is_date_valid(date.day, date.month, date.year):
            bot.send_message(message.from_user.id,  'Спасибо записал. Теперь введи дату выселения\n'
                                                    'Правильный формат: dd.mm.yyyy\n')
            bot.set_state(message.from_user.id, HotelInfoState.date_chack_out, message.chat.id)
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                check_in_dict = dict()
                check_in_dict["day"] = date.day
                check_in_dict["month"] = date.month
                check_in_dict["year"] = date.year
                data['check_in_date'] = check_in_dict

        else:
            bot.send_message(message.from_user.id, 'Неверный ввод даты. Попробуйте еще раз\n'
                                                   'Правильный формат: dd.mm.yyyy или dd-mm-yyyy\n')
    except ValueError:
        bot.send_message(message.from_user.id, 'Неверный ввод даты. Попробуйте еще раз\n'
                                               'Правильный формат: dd.mm.yyyy или dd-mm-yyyy\n')

@bot.message_handler(state=[HotelInfoState.date_chack_out])
def get_check_out_date(message: Message) -> None:

    """
    :get_min_price: обработчик ожидает сообщение
                  с датой выселения.
                  Проверяется корректность ввода даты, с помощью методов класса Date
                  Если дата была введена не корректно, блок сценария повторяется.
                  После чего предлагается ввести новое сообщение и вызывается
                  обработчик для выполнения следующего блока сценария

    :param message: объект pyTelegramBotApi
    :return: None
    """

    try:
        date = Date.from_string(message.text)
        if Date.is_date_valid(date.day, date.month, date.year):
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:

                check_out_dict = dict()
                check_out_dict["day"] = date.day
                check_out_dict["month"] = date.month
                check_out_dict["year"] = date.year
                data['check_out_date'] = check_out_dict
            bot.send_message(message.from_user.id, 'Спасибо записал. Теперь введи количество взрослых')
            bot.set_state(message.from_user.id, HotelInfoState.adults, message.chat.id)
        else:
            bot.send_message(message.from_user.id, 'Неверный ввод даты. Попробуйте еще раз\n'
                                                   'Правильный формат: dd.mm.yyyy или dd-mm-yyyy\n')
    except ValueError:
        bot.send_message(message.from_user.id, 'Неверный ввод даты. Попробуйте еще раз\n'
                                               'Правильный формат: dd.mm.yyyy или dd-mm-yyyy\n')

@bot.message_handler(state=[HotelInfoState.adults])
def get_adults(message: Message) -> None:

    """
    :get_adults: обработчик ожидает сообщение
                  с количеством взрослых гостей.
                  Проверяется корректность ввода.
                  Если не корректно, блок сценария повторяется. В противном случае
                  После чего предлагается ввести новое сообщение и вызывается
                  функция для выполнения следующего блока сценария

    :param message: объект pyTelegramBotApi
    :return: None
    """

    if message.text.isdigit():
        bot.send_message(message.from_user.id, 'Спасибо записал. Теперь введи количество детей')
        bot.set_state(message.from_user.id, HotelInfoState.childrens, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            guests_list = []
            guests_list.append({'adults': int(message.text)})
            data['adults'] = guests_list
    else:
        bot.send_message(message.from_user.id, 'Количество может быть только числом, введите еще раз')

@bot.message_handler(state=[HotelInfoState.childrens])
def get_children(message: Message) -> None:

    """
    :get_children: обработчик ожидает сообщение
                  с количеством детей.
                  Проверяется корректность ввода.
                  Если не корректно, блок сценария повторяется.
                  Сценарий переходит к блоку где производится API запрос поиск отелей.
                  В случае если есть дети, сценарий переходит к дополнительному блоку где предлагается
                  ввести возраст каждого ребенка.


    :param message: объект pyTelegramBotApi
    :return: None
    """

    if message.text.isdigit():
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['children_count'] = int(message.text)
            if data['children_count'] > 0:
                data['children_age_list'] = list()
                bot.send_message(message.from_user.id, f'Введите возраст каждого ребенка:')
                bot.set_state(message.from_user.id, HotelInfoState.childrens_age, message.chat.id)
            else:
                msg = f'Страна поиска: {data["country"]}\n' \
                      f'Город поиска: {data["city"]}\n' \
                      f'Взрослые: {data["adults"]}\n' \
                      f'Минимальная цена: {data["min_price"]}\n' \
                      f'Максимальная цена: {data["max_price"]}\n' \
                      f'Дата заселения: {data["check_in_date"]}\n' \
                      f'Дата выселения: {data["check_out_date"]}\n'
                data['msg'] = msg
                bot.send_message(message.from_user.id, f'Спасибо за предоставленную информацию, ваши данные\n')
                bot.send_message(message.from_user.id, '{}'.format(msg))
                get_hotels_list(message, msg)
    else:
        bot.send_message(message.from_user.id, 'Количество может быть только числом, введите еще раз')

@bot.message_handler(state=[HotelInfoState.childrens_age])
def get_children_age_list(message: Message):

    """
    :get_children_age_list: обработчик ожидает сообщение
                  с возрастом первого ребенка.
                  Проверяется корректность ввода.
                  Если не корректно, блок сценария повторяется.
                  В случае если детей несколько, блок сценария повторяется пока не будет
                  введен возраст каждого ребенка.


    :param message: объект pyTelegramBotApi
    :return: None
    """

    if message.text.isdigit():
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['children_age_list'].append({"age": int(message.text)})
        if len(data['children_age_list']) == data['children_count']:
            data['adults'][0]["children"] = data['children_age_list']
            print(data['adults'])
            msg = 'Страна поиска: {}\n' \
                  'Город поиска: {}\n' \
                  'Взрослые: {}\n' \
                  'Дети: {}\n' \
                  'Минимальная цена: {}\n' \
                  'Максимальная цена: {}\n' \
                  'Дата заселения: {}\n' \
                  'Дата выселения: {}\n'.format(data['country'],
                                                data['city'],
                                                data['adults'][0]["adults"],
                                                data['children_count'],
                                                data['min_price'],
                                                data['max_price'],
                                                data['check_in_date'],
                                                data['check_out_date'])
            bot.send_message(message.from_user.id, f'Спасибо за предоставленную информацию, '
                                                   f'ваши данные:\n')
            bot.send_message(message.from_user.id, '{}'.format(msg))
            get_hotels_list(message, msg)
        else:
            bot.send_message(message.chat.id, f'Введите возраст {len(data["children_age_list"])+1}-го ребенка:')
            bot.set_state(message.from_user.id, HotelInfoState.childrens_age, message.chat.id)

    else:
        bot.send_message(message.from_user.id, 'Количество может быть только числом, введите еще раз')


def get_hotels_list(message: Message, msg: str) -> None:

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

    try:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            create_json_with_hotels_propertys = HotelsID.set_propertys()
            create_json_with_hotels_propertys(
                 data['city_id'][0],
                 date_in=data['check_in_date'],
                 date_out=data['check_out_date'],
                 guests=data['adults'],
                 min_price=data['min_price'],
                 max_price=data['max_price'])

            hotels_list = HotelsID.get_hotels_list()
            hotels_list = hotels_list()
            print('ID города {}. название {}'.format(data['city_id'][0], data['city_id'][1]))
        bot.send_message(message.from_user.id, f'Список найденных отелей:\n')
        bot_message = ''
        for string in hotels_list:
            bot.send_message(message.from_user.id, f'Код - {string[0]}\n'
                                                   f'Название - {string[1]}\n'
                                                   f'Стоимость - {string[2]}\n')
            bot_message += f'Код - {string[0]}\n' \
                           f'Название - {string[1]}\n' \
                           f'Стоимость - {string[2]}\n'

        data_db = [{"chat_id": message.chat.id,
                 "user_name": message.from_user.username,
                 "user_request": msg,
                 "bot_response": bot_message}]
        db_write(db, History, data_db)
        bot.send_message(message.from_user.id, f'Хотите посмотреть подробную информацию о конкретном отеле: да/нет\n')
        bot.set_state(message.from_user.id, HotelInfoState.stop_or_continue, message.chat.id)

    except TypeError:
        bot.send_message(message.from_user.id, f'Что то пошло не так, попробуйте сделать запрос снова\n'
                                               f'Введите минимальную цену за отель')
        bot.set_state(message.from_user.id, HotelInfoState.min_price, message.chat.id)


@bot.message_handler(state=[HotelInfoState.stop_or_continue])
def stop_or_continue(message: Message) -> None:
    """
    :stop_or_continue: обработчик ожидает сообщение:
                  да/нет.
                  Проверяется корректность ввода,
                  если пользователь отвечает "да", то предлагается ввести код заинтересовавшего
                  отеля, и сценарий переходит к следующему блоку
                  если пользователь отвечает "нет" то сценарий завершается

    :param message: объект pyTelegramBotApi
    :return: None
    """

    if message.text.lower() == 'да':
        bot.send_message(message.from_user.id, f'Введите код отеля\n')
        bot.set_state(message.from_user.id, HotelInfoState.get_hotel_info, message.chat.id)
    elif message.text.lower() == 'нет':
        bot.send_message(message.from_user.id, f'Спасибо {message.from_user.username}\n'
                                               f'Поиск отелей завершен. Можете воспользоваться'
                                               f' другими функциями нажав кнопку "menu"\n')
        bot.delete_state(message.from_user.id, message.chat.id)

    else:
        bot.send_message(message.from_user.id, f'неверный ввод, введите да или нет\n')

@bot.message_handler(state=[HotelInfoState.get_hotel_info])
def get_hotel_info(message: Message) -> None:

    """
    :get_hotel_info: обработчик ожидает сообщение с кодом отеля.
                     Производится попытка сделать API запрос
                     в случае успеха пользователю отправляется подробная информация об отеле:
                     - точный адрес,
                     - местоположение на карте,
                     - фотографии.

    :param
        message: объект pyTelegramBotApi
    :return: None
    """
    try:
        info = deteil_info(message.text)
        if not info:
            raise Exception
        bot.send_message(message.from_user.id, f'Адрес отеля {info[0]}\n'
                                               f'Локация на карте {info[1]}\n')
        for photo in info[2]:
            bot.send_message(message.from_user.id, f'{photo[0]}\n'
                                                   f'{photo[1]}\n')
        bot.send_message(message.from_user.id,
                         f'Хотите еще посмотреть подробную информацию о конкретном отеле: да/нет\n')
        bot.set_state(message.from_user.id, HotelInfoState.stop_or_continue, message.chat.id)

    except Exception:
        bot.send_message(message.from_user.id,
                         f'Сервер не распознал введенный код, попробуйте еще раз\n')
        bot.set_state(message.from_user.id, HotelInfoState.get_hotel_info, message.chat.id)
