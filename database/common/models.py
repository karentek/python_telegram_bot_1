import peewee as pw
from datetime import datetime

db = pw.SqliteDatabase('database.db')

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



