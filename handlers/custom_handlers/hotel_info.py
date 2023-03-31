from loader import bot
from telebot.types import Message
from utils.surch.deteil_hotel_info import deteil_info
from states.hotel_information import HotelInfoState


@bot.message_handler(commands=["info_about_hotel"])
def choose_hotel(message: Message) -> None:

    """
    Сценарий обработчиков сообщений запускается командой info_about_hotel
    в данном блоке пользователю предлагается ввести код отеля
    для просмотра подробной информации о нем.
    Коды отелей можно взять из истории запросов.
    Данный модуль предназначен для тех, кому лень заново
    вбивать поисковую информацию и добывать коды отелей.

    :param message: объект pyTelegramBotApi
    :return: None
    """

    bot.set_state(message.from_user.id, HotelInfoState.get_hotel_info, message.chat.id)
    bot.send_message(message.from_user.id, f'{message.from_user.username}, введи код отеля')


@bot.message_handler(state=[HotelInfoState.get_hotel_info])
def get_hotel_info(message: Message) -> None:

    """
    :get_hotel_info: обработчик ожидает сообщение с кодом отеля.
                     Производится попытка сделать API запрос
                     в случае успеха пользователю отправляется подробная информация об отеле:
                     - точный адрес,
                     - местоположение на карте,
                     - фотографии.

    :param
        message: объект pyTelegramBotApi
    :return: None
    """
    try:
        info = deteil_info(message.text)
        if not info:
            raise Exception
        bot.send_message(message.from_user.id, f'Адрес отеля {info[0]}\n'
                                               f'Локация на карте {info[1]}\n')
        for photo in info[2]:
            bot.send_message(message.from_user.id, f'{photo[0]}\n'
                                                   f'{photo[1]}\n')
        bot.send_message(message.from_user.id,
                         f'Хотите еще посмотреть подробную информацию о конкретном отеле: да/нет\n')
        bot.set_state(message.from_user.id, HotelInfoState.stop_or_continue, message.chat.id)

    except Exception:
        bot.send_message(message.from_user.id,
                         f'Сервер не распознал введенный код, попробуйте ввести еще раз\n')
        bot.set_state(message.from_user.id, HotelInfoState.get_hotel_info, message.chat.id)



@bot.message_handler(state=[HotelInfoState.stop_or_continue])
def stop_or_continue(message: Message) -> None:
    """
    :stop_or_continue: обработчик ожидает сообщение:
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
        bot.set_state(message.from_user.id, HotelInfoState.get_hotel_info, message.chat.id)
    elif message.text.lower() == 'нет':
        bot.send_message(message.from_user.id, f'Спасибо {message.from_user.username}\n'
                                               f'Поиск отелей завершен. Можете воспользоваться'
                                               f' другими функциями нажав кнопку "menu"\n')
        bot.delete_state(message.from_user.id, message.chat.id)

    else:
        bot.send_message(message.from_user.id, f'неверный ввод, введите да или нет\n')

