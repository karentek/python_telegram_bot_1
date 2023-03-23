from telebot.handler_backends import State, StatesGroup

# 1 имя
# 2 возраст
# 3 страна
# 4 город
# 5 номер телефона

class UserInfoState(StatesGroup):
    name = State()
    age = State()
    country = State()
    city = State()
    number = State()
