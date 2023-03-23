from python_basic_diploma.utils.surch.API_request import ApiInterface
import json
from typing import Tuple, List


def _hotels_propertys(region_id: str, adults: int = 1, min_price: int = 1, max_price: int = 1000) -> None:

    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "destination": {"regionId": region_id},
        "checkInDate": {
            "day": 10,
            "month": 10,
            "year": 2022
        },
        "checkOutDate": {
            "day": 15,
            "month": 10,
            "year": 2022
        },
        "rooms": [
            {
                "adults": 2, None: None
                # "children": [{"age": 5}, {"age": 7}]
            }
        ],
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
    with open("V2_LIST.json", "w") as file:
        json.dump(responce, file, indent=4)


def _hotels_list() -> List[Tuple[str, str, str]]:
    with open("V2_LIST.json", "r", encoding='UTF-8') as file_v2:
        responce = json.load(file_v2)

        filtered_properties = [(item.get('id'), item.get('name'), str(int(item['price']['lead']['amount']))) for item in
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
