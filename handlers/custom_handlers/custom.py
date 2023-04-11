from loader import bot
from telebot.types import Message
from utils.surch.hotels_by_city import LocationID
from utils.surch.hotels_list import HotelsID
from utils.check_date import Date
from database.common.models import db, History, Flag, db_unicodes
from database.core import crud
from utils.surch.deteil_hotel_info import deteil_info
from states.hotel_information import HotelInfoState


db_write = crud.create()

@bot.message_handler(commands=["custom"])
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
                print(id)
                if not id:
                    raise Exception
                data['city_id'] = id
                print(data['city_id'])
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
                msg = '{} - {}\n' \
                      'Взрослые - {}\n' \
                      'Диапазон цен: {} - {}\n' \
                      'Даты пребывания: {}.{}.{} ' \
                      '- {}.{}.{}\n'.format(
                                            data['country'], data['city'],
                                            data['adults'][0]["adults"],
                                            data['min_price'], data['max_price'],
                                            data['check_in_date']['day'], data['check_in_date']['month'], data['check_in_date']['year'],
                                            data['check_out_date']['day'], data['check_out_date']['month'], data['check_out_date']['year']
                )

                data['msg'] = msg
                bot.send_message(message.chat.id, f'Сколько отелей вывести в результате?\nМаксимум 10')
                bot.set_state(message.from_user.id, HotelInfoState.hotels_count, message.chat.id)

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
            msg = '{} - {}\n' \
                  'Взрослые - {}, дети - {}\n' \
                  'Диапазон цен: {} - {}\n' \
                  'Даты пребывания: {}.{}.{} - {}.{}.{}\n'.format(
                                                data['country'], data['city'],
                                                data['adults'][0]["adults"], data['children_count'],
                                                data['min_price'], data['max_price'],
                                                data['check_in_date']['day'], data['check_in_date']['month'], data['check_in_date']['year'],
                                                data['check_out_date']['day'], data['check_out_date']['month'], data['check_out_date']['year'])
            data['msg'] = msg
            bot.send_message(message.chat.id, f'Сколько отелей вывести в результате?\nМаксимум 10')
            bot.set_state(message.from_user.id, HotelInfoState.hotels_count, message.chat.id)
        else:
            bot.send_message(message.chat.id, f'Введите возраст {len(data["children_age_list"])+1}-го ребенка:')
            bot.set_state(message.from_user.id, HotelInfoState.childrens_age, message.chat.id)

    else:
        bot.send_message(message.from_user.id, 'Количество может быть только числом, введите еще раз')


@bot.message_handler(state=[HotelInfoState.hotels_count])
def get_hotels_count(message: Message) -> None:
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

        bot.send_message(message.from_user.id, 'Спасибо записал. Сколько фотографий вывести к каждому отелю'
                                               '\nМаксимум 10')
        bot.set_state(message.from_user.id, HotelInfoState.photos_count, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            if 0 < int(message.text) <= 10:
                data['hotels_count'] = int(message.text)
            else:
                data['hotels_count'] = 10
    else:
        bot.send_message(message.from_user.id, 'Количество может быть только числом, попробуйте ввести еще раз')

@bot.message_handler(state=[HotelInfoState.photos_count])
def get_photos_count(message: Message) -> None:
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
        bot.send_message(message.from_user.id, 'Спасибо записал. Формирую список отелей...')
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            if 0 < int(message.text) <= 10:
                data['photos_count'] = int(message.text)
            else:
                data['photos_count'] = 10
        get_hotels_list(message)
    else:
        bot.send_message(message.from_user.id, 'Количество может быть только числом, попробуйте ввести еще раз')



def get_hotels_list(message: Message) -> None:

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
        country_code = data['city_id'][2]
        retrieved = Flag.select().where(Flag.country_name == country_code).get()

        if retrieved:
            flag = retrieved.iso_code
        else:
            flag = '***'
        if len(hotels_list) < data['hotels_count']:
            data['hotels_count'] = len(hotels_list)
        for i_count in range(0, data['hotels_count']):
            info = deteil_info(hotels_list[i_count][0])
            bot.send_message(message.from_user.id, f'{flag} {flag} {flag} Отель №{i_count + 1} {flag} {flag} {flag}\n'
                                                   f'{hotels_list[i_count][1]} - '
                                                   f'${hotels_list[i_count][2]}\n'
                                                   f'До центра города - {hotels_list[i_count][3]} км.\n'
                                                   f'Адрес отеля {info[0]}\n')
            if data['photos_count'] > 0:
                for i_photo in range(0, data['photos_count']):
                    bot.send_message(message.from_user.id, f'{info[2][i_photo]}\n')

            bot_message += f'{flag} {flag} {flag} Отель №{i_count + 1} {flag} {flag} {flag}\n' \
                           f'\n' \
                           f'{hotels_list[i_count][1]} - ' \
                           f'${hotels_list[i_count][2]}\n' \
                           f'До центра города - {hotels_list[i_count][3]} км.\n' \
                           f'Код отеля: {hotels_list[i_count][0]}\n' \
                           f'\n'

        data_db = [{
                 "chat_id": message.chat.id,
                 "user_name": message.from_user.username,
                 "user_request": data['msg'],
                 "bot_response": bot_message}]

        db_write(db, History, data_db)
        bot.send_message(message.from_user.id, f'Для дальнейшей работы выберите пункт меню')
        bot.delete_state(message.from_user.id, message.chat.id)

    except TypeError:
        bot.send_message(message.from_user.id, f'Что то пошло не так, попробуйте сделать запрос снова\n'
                                               f'Введите минимальную цену за отель')
        bot.set_state(message.from_user.id, HotelInfoState.min_price, message.chat.id)
