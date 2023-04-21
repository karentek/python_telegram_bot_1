from telebot.handler_backends import State, StatesGroup


class HighLowFunc(StatesGroup):
    country_h = State()
    city_h = State()
    country_l = State()
    city_l = State()
