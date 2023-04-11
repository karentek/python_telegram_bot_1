from . API_request import ApiInterface
import json
from typing import Tuple, List, Dict
import os

path = os.path.abspath(os.path.join('utils', 'files', 'hotels_list.json'))

def _hotels_propertys(region_id: str, guests: List[Dict], date_in: Dict, date_out: Dict, min_price: int = 1, max_price: int = 1000) -> None:

    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "ru_RU",
        "siteId": 300000001,
        "destination": {"regionId": region_id},
        "checkInDate": date_in,
        "checkOutDate": date_out,
        "rooms": guests,
        "resultsStartingIndex": 0,
        "resultsSize": 200,
        "sort": "PRICE_LOW_TO_HIGH",
        "filters": {"price": {
            "max": max_price,
            "min": min_price
        }}
    }
    request = ApiInterface.super_request()
    responce = request('/properties/v2/list', 'POST', payload)
    with open(path, "w+") as file:
        json.dump(responce, file, indent=4)


def _hotels_list() -> List[Tuple[str, str, str, float]]:
    with open(path, "r", encoding='UTF-8') as file_v2:
        responce = json.load(file_v2)

        filtered_properties = [(item.get('id'), item.get('name'), str(int(item['price']['lead']['amount'])), item['destinationInfo']['distanceFromDestination']['value']) for item in
                               responce['data']['propertySearch']['properties']]
        for string in filtered_properties:
            print(string)

    return filtered_properties


class HotelsID:

    @staticmethod
    def set_propertys():
        return _hotels_propertys

    @staticmethod
    def get_hotels_list():
        return _hotels_list
