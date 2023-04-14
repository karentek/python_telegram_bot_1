import peewee as pw
from datetime import datetime
import os
import pandas as pd
from loguru import logger


path_hotels = os.path.abspath(os.path.join('utils', 'files', 'database.db'))
path_unicodes = os.path.abspath(os.path.join('utils', 'files', 'unicodes.db'))
db = pw.SqliteDatabase(path_hotels)
db_unicodes = pw.SqliteDatabase(path_unicodes)




class ModelBase(pw.Model):
    """Базовая модель БД peewee"""
    created_at = pw.DateField(default=datetime.now())
    class Meta():
        database = db

class History(ModelBase):
    """
    Модель БД History содержит в себе поля:
        chat_id (str): id чата
        user_name (str): имя пользователя
        user_request (str): поисковый запрос пользователя
        bot_response (str): список отелей найденных по запросу пользователя
    """

    chat_id = pw.IntegerField()
    user_name = pw.TextField()
    user_request = pw.TextField()
    bot_response = pw.TextField()


class Flag(pw.Model):
    unicode = pw.CharField()
    iso_code = pw.CharField()
    country_name = pw.CharField()

    class Meta:
        database = db_unicodes


if not Flag.table_exists():
    logger.info("Создаем базу данных с флагами")

    Flag.create_table()
    tables = pd.read_html('https://unicode.bootstrap-4.ru/emoji/flags/')
    tables[1].drop(('№'), axis=1, inplace=True)
    tables[1].drop(('Картинка'), axis=1, inplace=True)
    tables[1].drop(axis=0, index=[0], inplace=True)
    for index, row in tables[1].iterrows():
        unicode = row['Юникод']
        iso_code = row['Символ']
        country_name = row['Описание'].replace('flag: ', '')
        flag = Flag(unicode=unicode, iso_code=iso_code, country_name=country_name)
        flag.save()

