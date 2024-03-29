import os
from . API_request import ApiInterface
import json
from typing import Tuple
from loguru import logger


path = os.path.abspath(os.path.join('utils', 'files', 'hotels_by_city.json'))
path_log = os.path.abspath(os.path.join('utils', 'files', 'file.log'))
logger.add(path_log, rotation="500 MB")


def _request_location(city: str, locale: str) -> None:
    logger.info("Запущена функция для запроса города поиска")
    querystring = {"q": city, "locale": locale}
    request = ApiInterface.super_request()
    responce = request('/locations/v3/search', 'GET', querystring)
    with open(path, "w+") as file:
        logger.info("Создан json файл hotels_by_city")
        json.dump(responce, file, indent=4)

def _find_location_id() -> Tuple[str, str, str]:
    logger.info("Запущена функция для парсинга json файла hotels_by_city, для поиска id города")
    with open(path, 'r') as file_v3:
        data = json.load(file_v3)
    city_id = data['sr'][0]["gaiaId"]
    city_name = data['sr'][0]["regionNames"]["shortName"]
    flag = data['sr'][0]["hierarchyInfo"]["country"]["name"]
    return city_id, city_name, flag


class LocationID:

    @staticmethod
    def set_city():
        return _request_location

    @staticmethod
    def get_id():
        return _find_location_id

