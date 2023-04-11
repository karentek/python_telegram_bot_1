from telebot import State
from telebot.handler_backends import State, StatesGroup


class HotelInfoState(StatesGroup):
    country = State()
    city = State()
    date_chack_in = State()
    date_chack_out = State()
    adults = State()
    childrens = State()
    min_price = State()
    max_price = State()
    childrens_age = State()
    stop_or_continue = State()
    get_hotel_info = State()
    best_deel = State()
    photos_count = State()
    hotels_count = State()
    tester_state = State()



