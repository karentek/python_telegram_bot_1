from typing import Dict, List, TypeVar
from ..common.models import db
from ..common.models import ModelBase
from peewee import ModelSelect


T = TypeVar('T')

def _store_data(db: db, model: T, *data: List[Dict]) -> None:
    with db.atomic():
        model.insert_many(*data).execute()

def _retrieve_data(db: db, model: T, *columns: ModelBase) -> ModelSelect:
    with db.atomic():
        response = model.select(*columns)
    return response


class CRUDInterface():

    @staticmethod
    def create():
        return _store_data

    @staticmethod
    def retrieve():
        return _retrieve_data