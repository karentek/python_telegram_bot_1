from python_basic_diploma.loader import bot
from python_basic_diploma.states.hotel_information import HotelInfoState
from telebot.types import Message


@bot.message_handler(commands=["choose_a_hotel"])
def choose_hotel(message: Message) -> None:
    bot.set_state(message.from_user.id, HotelInfoState.country, message.chat.id)
    bot.send_message(message.from_user.id, f'{message.from_user.username}, введи страну для поиска отеля')


@bot.message_handler(state=[HotelInfoState.country])
def get_country_(message: Message) -> None:
    bot.send_message(message.from_user.id, 'Спасибо записал. Теперь введи город')
    bot.set_state(message.from_user.id, HotelInfoState.city, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as hotel_data:
        hotel_data['country'] = message.text

@bot.message_handler(state=[HotelInfoState.city])
def get_city_(message: Message) -> None:
    bot.send_message(message.from_user.id, 'Спасибо записал. Теперь введи минимальную стоимость')
    bot.set_state(message.from_user.id, HotelInfoState.min_price, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as hotel_data:
        hotel_data['city'] = message.text


@bot.message_handler(state=[HotelInfoState.min_price])
def get_min_price(message: Message) -> None:
    if message.text.isdigit():
        bot.send_message(message.from_user.id, 'Спасибо записал. Теперь введи максимальную стоимость')
        bot.set_state(message.from_user.id, HotelInfoState.max_price, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as hotel_data:
            hotel_data['min_price'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Цена может быть только числом')

@bot.message_handler(state=[HotelInfoState.max_price])
def get_max_price(message: Message) -> None:
    if message.text.isdigit():
        bot.send_message(message.from_user.id, 'Спасибо записал. Теперь введи колличество взрослых')
        bot.set_state(message.from_user.id, HotelInfoState.adults, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as hotel_data:
            hotel_data['max_price'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Цена может быть только числом')


@bot.message_handler(state=[HotelInfoState.adults])
def get_adults(message: Message) -> None:
    if message.text.isdigit():
        bot.send_message(message.from_user.id, 'Спасибо записал. Теперь введи колличество детей')
        bot.set_state(message.from_user.id, HotelInfoState.childrens, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as hotel_data:
            hotel_data['adults'] = int(message.text)
    else:
        bot.send_message(message.from_user.id, 'Колличество может быть только числом')

# "children": [{"age": 5}, {"age": 7}]


@bot.message_handler(state=[HotelInfoState.childrens])
def get_childrens(message: Message) -> None:
    if message.text.isdigit():
        bot.send_message(message.from_user.id, 'Спасибо записал')
        with bot.retrieve_data(message.from_user.id, message.chat.id) as hotel_data:
            hotel_data['childrens'] = int(message.text)

        if int(message.text) > 0:
            bot.send_message(message.from_user.id, 'Введите возраст ребенка')
            bot.set_state(message.from_user.id, HotelInfoState.childrens_age, message.chat.id)
        elif int(message.text) == 0:
            bot.send_message(message.from_user.id, f'Спасибо за предоставленную информацию, ваши данные\n')
            for key, value in hotel_data.items():
                bot.send_message(message.from_user.id, f'{key}---{value}\n')
            bot.delete_state(message.from_user.id, message.chat.id)

    else:
        bot.send_message(message.from_user.id, 'Колличество может быть только числом')


age_list = []
@bot.message_handler(state=[HotelInfoState.childrens])
def get_childrens_age(message: Message) -> None:
    if message.text.isdigit():
        get_childrens_age.count = (int(message.text))
        bot.send_message(message.from_user.id, 'Спасибо записал')
        if get_childrens_age.count > 0:
            get_childrens_age.count -= 1
            bot.send_message(message.from_user.id, 'Введите возраст ребенка')
            bot.set_state(message.from_user.id, HotelInfoState.childrens_age, message.chat.id)
            age_list.append({"age": int(message.text)})
            with bot.retrieve_data(message.from_user.id, message.chat.id) as hotel_data:
                hotel_data["children"] = age_list
        else:
            for key, value in hotel_data.items():
                bot.send_message(message.from_user.id, f'{key}---{value}\n')


        bot.send_message(message.from_user.id, f'Спасибо за предоставленную информацию, ваши данные\n')
        bot.delete_state(message.from_user.id, message.chat.id)
