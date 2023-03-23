import peewee as pw
from datetime import datetime

db = pw.SqliteDatabase('database.db')

class ModelBase(pw.Model):
    created_at = pw.DateField(default=datetime.now())
    class Meta():
        database = db

class History(ModelBase):
    user_message = pw.TextField()
    bot_message = pw.TextField()
