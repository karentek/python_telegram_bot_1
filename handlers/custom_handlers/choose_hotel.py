from python_basic_diploma.loader import bot
from telebot.types import Message
from python_basic_diploma.utils.surch.hotels_by_city import LocationID
from python_basic_diploma.utils.surch.hotels_list import HotelsID
from typing import Dict
from python_basic_diploma.utils.check_date import Date
from python_basic_diploma.database.common.models import db, History
from python_basic_diploma.database.core import crud
from python_basic_diploma.utils.surch.deteil_hotel_info import deteil_info


class UserRequest:

    """
    Класс UserRequest: В атрибутах класса хранятся данные введенные пользователем
                        для доступа к ним из любого блока сценария выбора отеля
    """

    def __init__(self, chat_id: int, user_name: str) -> None:
        self.user_name = user_name
        self.chat_id = chat_id
        self.country = None
        self.city = None
        self.city_id = None
        self.max_price = None
        self.min_price = None
        self.adults = None
        self.children_count = None
        self.children_age_list = None
        self.hotels_list = None
        self.check_in_date = None
        self.check_out_date = None


dict_requests: Dict[int, UserRequest] = {}
db_write = crud.create()

@bot.message_handler(commands=["choose_a_hotel"])
def choose_hotel(message: Message) -> None:

    """
    Бот ожидает запуска сценария с сообщения с командой choose_a_hotel
    в данном блоке пользователю необходимо ввести название страны для последующуй обработки в
    следующем шаге сценария

    :param message: объект pyTelegramBotApi
    :return: None
    """

    bot.send_message(message.from_user.id, f'{message.from_user.username}, введи страну для поиска отеля')
    bot.register_next_step_handler(message, get_country_)


def get_country_(message: Message) -> None:

    """
    :get_country_: функция, на вход подается сообщение от пользователя с наименованием страны
                  проверяется правильность ввода, а именно:
                  сообщение должно состоять только из букв.
                  Если условие не выполняется, блок сценария повторяется.
                  Далее для данного чата создается объект класса UserRequest,
                  помещается в список для хранения,
                  и записываются данные в атрибуты класса.
                  После чего предлагается ввести новое сообщение и вызывается
                  функция для выполнения следующего блока сценария

    :param message: объект pyTelegramBotApi
    :return: None
    """

    if message.text.isalpha():
        instance = UserRequest(message.chat.id, message.from_user.username)
        instance.country = message.text
        dict_requests[message.chat.id] = instance
        bot.send_message(message.from_user.id, 'Спасибо записал. Теперь введи город')
        bot.register_next_step_handler(message, get_city_)
    else:
        bot.send_message(message.from_user.id, 'Можно вводить только буквы, повтори еще раз')
        bot.register_next_step_handler(message, choose_hotel)


def get_city_(message: Message) -> None:
    """
    :get_country_: функция, на вход подается сообщение от пользователя с наименованием города.
                  Проверяется правильность ввода, а именно:
                  сообщение должно состоять только из букв.
                  Если условие не выполняется, блок сценария повторяется.
                  В случае успешной проверки
                  производится попытка совершить API запрос, обработать полученный JSON,
                  и извлечь ID искомого города, в случае неудачной попытки вызывается ошибка,
                  после чего предлагается начать заново ввод данных.
                  Данные записываются в атрибуты класса.
                  Далее предлагается ввести новое сообщение и вызывается
                  функция для выполнения следующего блока сценария

    :param message:
    :return:
    """
    if message.text.isalpha():
        try:
            instance = dict_requests[message.chat.id]
            instance.city = message.text
            create_json_with_location_id = LocationID.set_city()
            create_json_with_location_id(instance.city, instance.country)
            get_location_id = LocationID.get_id()
            id = get_location_id()
            if not id:
                raise Exception
            instance.city_id = id
            bot.send_message(message.from_user.id, 'Спасибо записал. Теперь введи минимальную стоимость')
            bot.register_next_step_handler(message, get_min_price)
        except Exception:
            bot.send_message(message.from_user.id, 'Произошла ошибка, видимо такой локации не существует\n'
                                                   'Попробуйте заново\n'
                                                   'Введите страну поиска')
            bot.register_next_step_handler(message, get_country_)

    else:
        bot.send_message(message.from_user.id, 'Можно вводить только буквы, повтори еще раз')
        bot.register_next_step_handler(message, get_city_)


def get_min_price(message: Message) -> None:
    """
    :get_min_price: функция, на вход подается сообщение
                  с минимальной приемлемой для пользователя стоимостью
                  проверяется правильность ввода, а именно:
                  сообщение должно состоять только из цифр.
                  Если условие не выполняется, блок сценария повторяется.
                  Данные записываются в атрибуты класса UserRequest.
                  После чего предлагается ввести новое сообщение и вызывается
                  функция для выполнения следующего блока сценария

    :param message: объект pyTelegramBotApi
    :return: None
    """

    instance = dict_requests[message.chat.id]
    if message.text.isdigit():
        instance.min_price = int(message.text)
        bot.send_message(message.from_user.id, 'Спасибо записал. Теперь введи максимальную стоимость')
        bot.register_next_step_handler(message, get_max_price)
    else:
        bot.send_message(message.from_user.id, 'Цена может быть только числом, попробуйте ввести еще раз')
        bot.register_next_step_handler(message, get_min_price)


def get_max_price(message: Message) -> None:

    """
    :get_min_price: функция, на вход подается сообщение
                  с максимальной приемлемой для пользователя стоимостью
                  проверяется правильность ввода, а именно:
                  сообщение должно состоять только из цифр.
                  Если условие не выполняется, блок сценария повторяется.
                  Данные записываются в атрибуты класса UserRequest.
                  После чего предлагается ввести новое сообщение и вызывается
                  функция для выполнения следующего блока сценария

    :param message: объект pyTelegramBotApi
    :return: None
    """

    instance = dict_requests[message.chat.id]
    if message.text.isdigit():
        instance.max_price = int(message.text)
        bot.send_message(message.from_user.id, 'Спасибо записал. Теперь введи дату заселения\n'
                                               'Правильный формат: dd.mm.yyyy\n')
        bot.register_next_step_handler(message, get_check_in_date)
    else:
        bot.send_message(message.from_user.id, 'Цена может быть только числом, попробуйте ввести еще раз')
        bot.register_next_step_handler(message, get_max_price)

def get_check_in_date(message: Message) -> None:

    """
    :get_min_price: функция, на вход подается сообщение
                  с датой заселения.
                  Проверяется корректность ввода даты, с помощью методов класса Date
                  Если дата была введена не корректно, блок сценария повторяется.
                  Данные записываются в атрибуты класса UserRequest.
                  После чего предлагается ввести новое сообщение и вызывается
                  функция для выполнения следующего блока сценария

    :param message: объект pyTelegramBotApi
    :return: None
    """

    try:
        date = Date.from_string(message.text)
        if Date.is_date_valid(date.day, date.month, date.year):
            instance = dict_requests[message.chat.id]
            check_in_dict = dict()
            check_in_dict["day"] = date.day
            check_in_dict["month"] = date.month
            check_in_dict["year"] = date.year
            instance.check_in_date = check_in_dict
            bot.send_message(message.from_user.id,  'Спасибо записал. Теперь введи дату выселения\n'
                                                    'Правильный формат: dd.mm.yyyy\n')
            bot.register_next_step_handler(message, get_check_out_date)
        else:
            bot.send_message(message.from_user.id, 'Неверный ввод даты. Попробуйте еще раз\n'
                                                   'Правильный формат: dd.mm.yyyy или dd-mm-yyyy\n')
            bot.register_next_step_handler(message, get_check_in_date)
    except ValueError:
        bot.send_message(message.from_user.id, 'Неверный ввод даты. Попробуйте еще раз\n'
                                               'Правильный формат: dd.mm.yyyy или dd-mm-yyyy\n')
        bot.register_next_step_handler(message, get_check_in_date)


def get_check_out_date(message: Message) -> None:

    """
    :get_min_price: функция, на вход подается сообщение
                  с датой выселения.
                  Проверяется корректность ввода даты, с помощью методов класса Date
                  Если дата была введена не корректно, блок сценария повторяется.
                  Данные записываются в атрибуты класса UserRequest.
                  После чего предлагается ввести новое сообщение и вызывается
                  функция для выполнения следующего блока сценария

    :param message: объект pyTelegramBotApi
    :return: None
    """

    try:
        date = Date.from_string(message.text)
        if Date.is_date_valid(date.day, date.month, date.year):
            instance = dict_requests[message.chat.id]
            check_out_dict = dict()
            check_out_dict["day"] = date.day
            check_out_dict["month"] = date.month
            check_out_dict["year"] = date.year
            instance.check_out_date = check_out_dict
            bot.send_message(message.from_user.id, 'Спасибо записал. Теперь введи количество взрослых')
            bot.register_next_step_handler(message, get_adults)
        else:
            bot.send_message(message.from_user.id, 'Неверный ввод даты. Попробуйте еще раз\n'
                                                   'Правильный формат: dd.mm.yyyy или dd-mm-yyyy\n')
            bot.register_next_step_handler(message, get_check_out_date)
    except ValueError:
        bot.send_message(message.from_user.id, 'Неверный ввод даты. Попробуйте еще раз\n'
                                               'Правильный формат: dd.mm.yyyy или dd-mm-yyyy\n')
        bot.register_next_step_handler(message, get_check_out_date)


def get_adults(message: Message) -> None:

    """
    :get_min_price: функция, на вход подается сообщение
                  с количеством взрослых гостей.
                  Проверяется корректность ввода.
                  Если не корректно, блок сценария повторяется.
                  Данные записываются в атрибуты класса UserRequest.
                  После чего предлагается ввести новое сообщение и вызывается
                  функция для выполнения следующего блока сценария

    :param message: объект pyTelegramBotApi
    :return: None
    """

    if message.text.isdigit():
        instance = dict_requests[message.chat.id]
        guests_list = []
        guests_list.append({'adults': int(message.text)})
        instance.adults = guests_list
        bot.send_message(message.from_user.id, 'Спасибо записал. Теперь введи количество детей')
        bot.register_next_step_handler(message, get_children)
    else:
        bot.send_message(message.from_user.id, 'Количество может быть только числом, введите еще раз')
        bot.register_next_step_handler(message, get_adults)


def get_children(message: Message) -> None:

    """
    :get_min_price: функция, на вход подается сообщение
                  с количеством детей гостей.
                  Проверяется корректность ввода.
                  Если не корректно, блок сценария повторяется.
                  В случае если детей нет то
                  данные записываются в атрибуты класса UserRequest.
                  Формируется с ними сообщение и отправляются пользователю,
                  и сценарий переходит к следующему блоку.
                  В случае если есть дети, сценарий переходит к дополнительному блоку где предлагается
                  ввести возраст каждого ребенка.


    :param message: объект pyTelegramBotApi
    :return: None
    """

    if message.text.isdigit():
        instance = dict_requests[message.chat.id]
        instance.children_count = int(message.text)
        if instance.children_count > 0:
            instance.children_age_list = list()
            bot.send_message(message.from_user.id, f'Введите возраст каждого ребенка:')
            bot.register_next_step_handler(message, get_children_age_list)
        else:
            msg = f'Страна поиска: {instance.country}\n' \
                  f'Город поиска: {instance.city}\n' \
                  f'Взрослые: {instance.adults}\n' \
                  f'Минимальная цена: {instance.min_price}\n' \
                  f'Максимальная цена: {instance.max_price}\n' \
                  f'Дата заселения: {instance.check_in_date}\n' \
                  f'Дата выселения: {instance.check_out_date}\n'
            bot.send_message(message.from_user.id, f'Спасибо за предоставленную информацию, ваши данные\n')
            bot.send_message(message.from_user.id, '{}'.format(msg))
            get_hotels_list(message, msg)
    else:
        bot.send_message(message.from_user.id, 'Количество может быть только числом, введите еще раз')
        bot.register_next_step_handler(message, get_children)


def get_children_age_list(message: Message):

    """
    :get_children_age_list: функция, на вход подается сообщение
                  с возрастом первого ребенка.
                  Проверяется корректность ввода.
                  Если не корректно, блок сценария повторяется.
                  В случае если ребенок один
                  данные записываются в атрибуты класса UserRequest.
                  Формируется с ними сообщение и отправляются пользователю,
                  и сценарий переходит к следующему блоку.
                  В случае если детей несколько, блок сценария повторяется пока не будет
                  введен возраст каждого ребенка.


    :param message: объект pyTelegramBotApi
    :return: None
    """

    if message.text.isdigit():
        instance = dict_requests[message.chat.id]
        instance.children_age_list.append({"age": int(message.text)})
        if len(instance.children_age_list) == instance.children_count:
            instance.adults[0]["children"] = instance.children_age_list
            print(instance.adults)
            msg = 'Страна поиска: {}\n' \
                  'Город поиска: {}\n' \
                  'Взрослые: {}\n' \
                  'Дети: {}\n' \
                  'Минимальная цена: {}\n' \
                  'Максимальная цена: {}\n' \
                  'Дата заселения: {}\n' \
                  'Дата выселения: {}\n'.format(instance.country,
                                                instance.city,
                                                instance.adults[0]["adults"],
                                                instance.children_count,
                                                instance.min_price,
                                                instance.max_price,
                                                instance.check_in_date,
                                                instance.check_out_date)
            bot.send_message(message.from_user.id, f'Спасибо за предоставленную информацию, '
                                                   f'ваши данные:\n')
            bot.send_message(message.from_user.id, '{}'.format(msg))
            get_hotels_list(message, msg)
        else:
            bot.send_message(message.chat.id, f'Введите возраст {len(instance.children_age_list)+1}-го ребенка:')
            bot.register_next_step_handler(message, get_children_age_list)
    else:
        bot.send_message(message.from_user.id, 'Количество может быть только числом, введите еще раз')
        bot.register_next_step_handler(message, get_children_age_list)


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
        instance = dict_requests[message.chat.id]
        create_json_with_hotels_propertys = HotelsID.set_propertys()
        create_json_with_hotels_propertys(
            instance.city_id[0],
            date_in=instance.check_in_date,
            date_out=instance.check_out_date,
            guests=instance.adults,
            min_price=instance.min_price,
            max_price=instance.max_price)

        hotels_list = HotelsID.get_hotels_list()
        hotels_list = hotels_list()
        print('ID города {}. название {}'.format(instance.city_id[0], instance.city_id[1]))
        bot.send_message(message.from_user.id, f'Список найденных отелей:\n')
        bot_message = ''
        for string in hotels_list:
            bot.send_message(message.from_user.id, f'Код - {string[0]}\n'
                                                   f'Название - {string[1]}\n'
                                                   f'Стоимость - {string[2]}\n')
            bot_message += f'Код - {string[0]}\n' \
                           f'Название - {string[1]}\n' \
                           f'Стоимость - {string[2]}\n'

        data = [{"chat_id": message.chat.id,
                 "user_name": message.from_user.username,
                 "user_request": msg,
                 "bot_response": bot_message}]
        db_write(db, History, data)
        bot.send_message(message.from_user.id, f'Хотите посмотреть подробную информацию о конкретном отеле: да/нет\n')
        bot.register_next_step_handler(message, stop_or_continue)

    except TypeError:
        bot.send_message(message.from_user.id, f'Что то пошло не так, попробуйте сделать запрос снова\n'
                                               f'Минимальную цену за отель')
        bot.register_next_step_handler(message, get_min_price)


def stop_or_continue(message: Message) -> None:
    """
    :stop_or_continue: функция, на вход подается сообщение:
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
        bot.register_next_step_handler(message, get_hotel_info)
    elif message.text.lower() == 'нет':
        bot.send_message(message.from_user.id, f'Спасибо {message.from_user.username}\n'
                                               f'Поиск отелей завершен. Можете воспользоваться'
                                               f' другими функциями нажав кнопку "menu"\n')
    else:
        bot.send_message(message.from_user.id, f'неверный ввод, введите да или нет\n')
        bot.register_next_step_handler(message, stop_or_continue)


def get_hotel_info(message: Message) -> None:

    """
    :get_hotel_info: функция, на вход подается сообщение с кодом отеля.
                     Производится попытка сделать API запрос
                     в случае успеха пользователю отправляется подробная информация об отеле:
                     точный адрес,
                     местоположение на карте,
                     фотографии.

                     После выдачи информации предлагается ввести код следующего отеля,
                     или завершить просмотр

                     Конец сценария.


    :param
        message: объект pyTelegramBotApi
    :return: None
    """

    info = deteil_info(message.text)
    bot.send_message(message.from_user.id, f'Адрес отеля {info[0]}\n'
                                           f'Локация на карте {info[1]}\n')
    for photo in info[2]:
        bot.send_message(message.from_user.id, f'{photo[0]}\n'
                                               f'{photo[1]}\n')
    bot.send_message(message.from_user.id, f'Хотите еще посмотреть подробную информацию о конкретном отеле: да/нет\n')
    bot.register_next_step_handler(message, stop_or_continue)
