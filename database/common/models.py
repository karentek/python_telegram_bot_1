import peewee as pw
from datetime import datetime

db = pw.SqliteDatabase('database.db')

class ModelBase(pw.Model):
    created_at = pw.DateField(default=datetime.now())
    class Meta():
        database = db

class History(ModelBase):
    chat_id = pw.TextField()
    user_name = pw.TextField()
    user_request = pw.TextField()
    bot_response = pw.TextField()


