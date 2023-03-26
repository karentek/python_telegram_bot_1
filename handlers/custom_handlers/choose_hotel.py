from python_basic_diploma.loader import bot
from python_basic_diploma.states.hotel_information import HotelInfoState
from telebot.types import Message
from python_basic_diploma.utils.surch.hotels_by_city import LocationID
from python_basic_diploma.utils.surch.hotels_list import HotelsID
from typing import Dict

# Создаем состояние, в котором мы ожидаем словарь

class UserRequest:
    def __init__(self, chat_id, user_name):
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

dict_requests: Dict[int, UserRequest] = {}

@bot.message_handler(commands=["choose_a_hotel"])
def choose_hotel(message: Message) -> None:

    bot.send_message(message.from_user.id, f'{message.from_user.username}, введи страну для поиска отеля')
    bot.register_next_step_handler(message, get_country_)


def get_country_(message: Message) -> None:
    instance = UserRequest(message.chat.id, message.from_user.username)
    instance.country = message.text
    dict_requests[message.chat.id] = instance
    bot.send_message(message.from_user.id, 'Спасибо записал. Теперь введи город')
    bot.register_next_step_handler(message, get_city_)


def get_city_(message: Message) -> None:
    instance = dict_requests[message.chat.id]
    instance.city = message.text
    create_json_with_location_id = LocationID.set_city()
    create_json_with_location_id(instance.city, instance.country)
    get_location_id = LocationID.get_id()
    id = get_location_id()
    instance.city_id = id
    bot.send_message(message.from_user.id, 'Спасибо записал. Теперь введи минимальную стоимость')
    bot.register_next_step_handler(message, get_min_price)


def get_min_price(message: Message) -> None:
    instance = dict_requests[message.chat.id]
    if message.text.isdigit():
        instance.min_price = int(message.text)
        bot.send_message(message.from_user.id, 'Спасибо записал. Теперь введи максимальную стоимость')
        bot.register_next_step_handler(message, get_max_price)
    else:
        bot.send_message(message.from_user.id, 'Цена может быть только числом')

def get_max_price(message: Message) -> None:
    instance = dict_requests[message.chat.id]

    if message.text.isdigit():
        instance.max_price = int(message.text)
        bot.send_message(message.from_user.id, 'Спасибо записал. Теперь введи колличество взрослых')
        bot.register_next_step_handler(message, get_adults)
    else:
        bot.send_message(message.from_user.id, 'Цена может быть только числом')


def get_adults(message: Message) -> None:
    instance = dict_requests[message.chat.id]

    guests_list = []
    if message.text.isdigit():
        guests_list.append({'adults': int(message.text)})
        instance.adults = guests_list
        bot.send_message(message.from_user.id, 'Спасибо записал. Теперь введи колличество детей')
        bot.register_next_step_handler(message, get_childrens)
    else:
        bot.reply_to(message.from_user.id, 'Колличество может быть только числом')

def get_childrens(message: Message) -> None:
    instance = dict_requests[message.chat.id]
    instance.children_count = int(message.text)

    if instance.children_count > 0:
        instance.children_age_list = list()
        bot.send_message(message.from_user.id, f'Введите возраст каждого ребенка:')
        bot.register_next_step_handler(message, get_children_age_list)

    else:
        bot.send_message(message.from_user.id, f'Спасибо за предоставленную информацию, ваши данные\n')
        bot.send_message(message.from_user.id, f'Страна поиска: {instance.country}\n'
                                               f'Город поиска: {instance.city}\n'
                                               f'Взрослые: {instance.adults}\n'
                                               f'Минимальная цена: {instance.min_price}\n'
                                               f'Максимальная цена: {instance.max_price}\n')

        create_json_with_hotels_propertys = HotelsID.set_propertys()
        create_json_with_hotels_propertys(
            instance.city_id[0],
            guests=instance.adults,
            min_price=instance.min_price,
            max_price=instance.max_price,

        )
        hotels_list = HotelsID.get_hotels_list()
        hotels_list = hotels_list()
        instance.hotels_list = hotels_list
        print('ID города {}. название {}'.format(instance.city_id[0], instance.city_id[1]))
        for string in hotels_list:
            print(string)


def get_children_age_list(message: Message):
    instance = dict_requests[message.chat.id]
    instance.children_age_list.append({"age": int(message.text)})
    if len(instance.children_age_list) == instance.children_count:
        instance.adults.append(instance.children_age_list)
        bot.send_message(message.from_user.id, f'Спасибо за предоставленную информацию, ваши данные:\n')
        bot.send_message(message.from_user.id, f'Страна поиска: {instance.country}\n'
                                               f'Город поиска: {instance.city}\n'
                                               f'Взрослые: {instance.adults[0]}\n'
                                               f'Дети: {instance.adults[1]}\n'
                                               f'Минимальная цена: {instance.min_price}\n'
                                               f'Максимальная цена: {instance.max_price}\n')
        create_json_with_hotels_propertys = HotelsID.set_propertys()
        create_json_with_hotels_propertys(
            instance.city_id[0],
            guests=instance.adults,
            min_price=instance.min_price,
            max_price=instance.max_price
        )
        hotels_list = HotelsID.get_hotels_list()
        hotels_list = hotels_list()
        print('ID города {}. название {}'.format(instance.city_id[0], instance.city_id[1]))
        for string in hotels_list:
            print(string)

    else:
        bot.send_message(message.chat.id, f'Введите возраст {len(instance.children_age_list)+1}-го ребенка:')
        bot.register_next_step_handler(message, get_children_age_list)



