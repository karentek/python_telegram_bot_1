from python_basic_diploma.loader import bot
from python_basic_diploma.states.hotel_information import HotelInfoState
from telebot.types import Message
from python_basic_diploma.utils.surch.hotels_by_city import LocationID
from python_basic_diploma.utils.surch.hotels_list import HotelsID


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
        create_json_with_location_id = LocationID.set_city()
        create_json_with_location_id(hotel_data['city'], hotel_data['country'])
        get_location_id = LocationID.get_id()
        id = get_location_id()
        hotel_data['cityID'] = id


@bot.message_handler(state=[HotelInfoState.min_price])
def get_min_price(message: Message) -> None:
    if message.text.isdigit():
        bot.send_message(message.from_user.id, 'Спасибо записал. Теперь введи максимальную стоимость')
        bot.set_state(message.from_user.id, HotelInfoState.max_price, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as hotel_data:
            hotel_data['min_price'] = int(message.text)
    else:
        bot.send_message(message.from_user.id, 'Цена может быть только числом')

@bot.message_handler(state=[HotelInfoState.max_price])
def get_max_price(message: Message) -> None:
    if message.text.isdigit():
        bot.send_message(message.from_user.id, 'Спасибо записал. Теперь введи колличество взрослых')
        bot.set_state(message.from_user.id, HotelInfoState.adults, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as hotel_data:
            hotel_data['max_price'] = int(message.text)
    else:
        bot.send_message(message.from_user.id, 'Цена может быть только числом')


@bot.message_handler(state=[HotelInfoState.adults])
def get_adults(message: Message) -> None:
    guests_list = []
    if message.text.isdigit():
        bot.send_message(message.from_user.id, 'Спасибо записал. Теперь введи колличество детей')
        bot.set_state(message.from_user.id, HotelInfoState.childrens, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as hotel_data:
            guests_list.append({'adults': int(message.text)})
            hotel_data['guests'] = guests_list
    else:
        bot.send_message(message.from_user.id, 'Колличество может быть только числом')

@bot.message_handler(state=[HotelInfoState.childrens])
def get_childrens(message: Message) -> None:
    children_count = int(message.text)
    if children_count > 0:
        bot.send_message(message.chat.id, f'Введите возраст каждого ребенка:')
        bot.register_next_step_handler(message, get_children_age_list, [], children_count)
        # bot.set_state(message.from_user.id, HotelInfoState.childrens_age, message.chat.id, get_children_age_list, [], children_count)

    else:
        bot.send_message(message.from_user.id, f'Спасибо за предоставленную информацию, ваши данные\n')
        with bot.retrieve_data(message.from_user.id, message.chat.id) as hotel_data:
            for key, value in hotel_data.items():
                bot.send_message(message.from_user.id, f'{key}---{value}\n')
            create_json_with_hotels_propertys = HotelsID.set_propertys()
            create_json_with_hotels_propertys(
                hotel_data['cityID'][0],
                guests=hotel_data['guests'],
                min_price=hotel_data['min_price'],
                max_price=hotel_data['max_price'],

            )
            hotels_list = HotelsID.get_hotels_list()
            hotels_list = hotels_list()
            hotel_data['hotels_list'] = hotels_list
            print('ID города {}. название {}'.format(hotel_data['cityID'], hotel_data['city']))
            for string in hotels_list:
                print(string)

        bot.delete_state(message.from_user.id, message.chat.id)

@bot.message_handler(state=[HotelInfoState.childrens])
def get_children_age_list(message, children_age_list, children_count):
    children_age_list.append({"age": int(message.text)})
    if len(children_age_list) == children_count:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as hotel_data:
            hotel_data['guests'].append(children_age_list)
            bot.send_message(message.from_user.id, f'Спасибо за предоставленную информацию, ваши данные:\n')
            for key, value in hotel_data.items():
                bot.send_message(message.from_user.id, f'{key}---{value}\n')
            create_json_with_hotels_propertys = HotelsID.set_propertys()
            create_json_with_hotels_propertys(
                hotel_data['cityID'][0],
                guests=hotel_data['guests'],
                min_price=hotel_data['min_price'],
                max_price=hotel_data['max_price'])
            hotels_list = HotelsID.get_hotels_list()
            hotels_list = hotels_list()
            hotel_data['hotels_list'] = hotels_list
            print('ID города {}. название {}'.format(hotel_data['cityID'], hotel_data['city']))
            for string in hotels_list:
                print(string)
            bot.delete_state(message.from_user.id, message.chat.id)

    else:
        bot.send_message(message.chat.id, f'Введите возраст {len(children_age_list)+1}-го ребенка:')
        bot.register_next_step_handler(message, get_children_age_list, children_age_list, children_count)



