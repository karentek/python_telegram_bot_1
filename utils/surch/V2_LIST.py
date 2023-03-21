from API_request import ApiInterface
import json
from typing import Tuple, List


def _hotels_propertys() -> None:
    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "destination": {"regionId": "553248635975177316"},
        "checkInDate": {
            "day": 25,
            "month": 3,
            "year": 2023
        },
        "checkOutDate": {
            "day": 26,
            "month": 3,
            "year": 2023
        },
        "rooms": [
            {
                "adults": 2,
                "children": [{"age": 5}, {"age": 7}]
            }
        ],
        "resultsStartingIndex": 0,
        "resultsSize": 200,
        "sort": "PRICE_LOW_TO_HIGH",
        "filters": {"price": {
            "max": 500,
            "min": 1
        }}
    }
    request = ApiInterface.super_request()
    responce = request('/properties/v2/list', 'POST', payload)
    with open("V2_LIST.json", "w") as file:
        json.dump(responce, file, indent=4)


def _hotels_list() -> List[Tuple[str, str, str]]:
    with open("V2_LIST.json", "r", encoding='UTF-8') as file_v2:
        responce = json.load(file_v2)

        filtered_properties = [
            (item.get('id'), item.get('name'), item['price']['strikeOut']['formatted'])
            for item in responce['data']['propertySearch']['properties']
        ]
        for string in filtered_properties:
            print(string)

    return filtered_properties


class HotelsID:

    @staticmethod
    def hotels_propertys():
        return _hotels_propertys

    @staticmethod
    def hotels_list():
        return _hotels_list
