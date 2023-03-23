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



