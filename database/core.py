from python_basic_diploma.database.common.models import db, History
from python_basic_diploma.database.utils.CRUD import CRUDInterface


db.connect()
db.create_tables([History])
crud = CRUDInterface()

if __name__ == '__main__':
    crud()