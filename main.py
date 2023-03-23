from python_basic_diploma.loader import bot
from python_basic_diploma import handlers  # noqa
from utils.set_bot_commands import set_default_commands

if __name__ == "__main__":
    set_default_commands(bot)
    bot.infinity_polling()
