# Python Diploma Basic





A simple Telegram bot for travelers that helps users find a hotel to their liking, and for entertainment has a game on board to memorize the flags of all countries in the world.

<img src="logo.png" width="300" height="300">

## Technologies used

- Python
- SQLite

## Getting started

To get started, follow these steps:

```
mkdir -p $PYTHONPATH/python_basic_diploma
cd $PYTHONPATH/python_basic_diploma
git clone https://gitlab.skillbox.ru/karen_teknedzhian/python_basic_diploma/-/tree/master
cd python_basic_diploma
source $YOUR_PYTHON_ENV/bin/activate
pip install -r requirements.txt
```

Make sure to add your own values to the `.env` file based on the `.env.template` file.

The following packages are needed and are included in `requirements.txt`:

- pyTelegramBotAPI==4.9.0
- python-dotenv==0.21.1
- peewee~=3.16.0
- python-telegram-bot-calendar
- requests~=2.28.2
- loguru

## Project structure

```
python_diploma_basic/           # Root directory of the project
├── config_data/
├── database/
├── handlers/
│   ├── custom_handlers/
│   └── default_handlers/
├── keyboards/
│   ├── inline/
│   └── reply/
├── states/
├── utils/
│   ├── files/
│   ├── misc/
│   └── surch/
├── .env
├── .env.template
├── .gitignore
├── loader.py
├── main.py
├── requirements.txt
└── __init__.py
```

## Features

The bot provides the following features:

- `/start`: The welcoming message.
- `/custom`: This command outputs a list of suitable hotels based on your request. The message contains the name, price, and distance to the city center.
- `/info_about_hotel`: This command outputs the exact address, location, and facilities of the hotel.
- `/highest_price`: This command outputs the hotel with the highest price based on your request.
- `/lowest_price`: This command outputs the hotel with the lowest price based on your request.
- `/game`: This command starts the game where the user can guess the flag of a random country.

## Authors

- Karen Teknedzhian

## License

This project is licensed under the MIT License - see the LICENSE file for details.