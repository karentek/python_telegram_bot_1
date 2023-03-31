from . API_request import ApiInterface
import json
from typing import Tuple


def _request_location(city: str, locale: str) -> None:

    querystring = {"q": city, "locale": locale}
    request = ApiInterface.super_request()
    responce = request('/locations/v3/search', 'GET', querystring)
    with open("hotels_by_city.json", "w") as file:
        json.dump(responce, file, indent=4)

def _find_location_id() -> Tuple[str, str]:

    with open('hotels_by_city.json', 'r') as file_v3:
        data = json.load(file_v3)
    city_id = data['sr'][0]["gaiaId"]
    city_name = data['sr'][0]["regionNames"]["shortName"]
    return city_id, city_name


class LocationID:

    @staticmethod
    def set_city():
        return _request_location

    @staticmethod
    def get_id():
        return _find_location_id
