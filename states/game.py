from telebot.handler_backends import State, StatesGroup


class Game(StatesGroup):
    entering_country = State()
    view_flag = State()
    check_country = State()
