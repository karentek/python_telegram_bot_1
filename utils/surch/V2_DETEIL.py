from API_request import ApiInterface
import json

def _deteil(id: str) -> None:
    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "propertyId": id
    }

    request = ApiInterface.super_request()
    responce = request('/properties/v2/detail', 'POST', payload)

    with open("V2_DETEIL.json", "w") as file:
        json.dump(responce, file, indent=4)

    with open("V2_DETEIL.json", "r") as file_v2D:
        json.load(file_v2D)

    #TODO Добавить фильтр для вывода инфо о найденном отеле


