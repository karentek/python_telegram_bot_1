import os
from . API_request import ApiInterface
import json
from typing import Tuple, List
from loguru import logger

path = os.path.abspath(os.path.join('utils', 'files', 'deteil_hotel_info.json'))

def _deteil(id: str) -> Tuple[str, str, List[Tuple[str, str]]]:
    logger.info("Запущена функция для отправки /properties/v2/detail' _deteil")

    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "ru_RU",
        "siteId": 300000001,
        "propertyId": id
    }

    request = ApiInterface.super_request()
    responce = request('/properties/v2/detail', 'POST', payload)

    with open(path, "w+") as file:
        json.dump(responce, file, indent=4)

    with open(path, "r") as file_v2D:
        logger.info("Запущена функция для парсинга deteil_hotel_info.json")

        response = json.load(file_v2D)
        adress = response['data']['propertyInfo']['summary']['location']['address']['addressLine']
        view_in_map_link = response['data']['propertyInfo']['summary']['location']['staticImage']['url']
        photos_list = response['data']['propertyInfo']['propertyGallery']['images']
        photos = [(photos_list[index]['image']['description'], photos_list[index]['image']['url']) for index in range(len(photos_list))]

    return adress, view_in_map_link, photos

class DeteilHotel:

    @staticmethod
    def deteil_hotel():
        return _deteil


deteil_info = DeteilHotel.deteil_hotel()

