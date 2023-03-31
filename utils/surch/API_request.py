import requests
from typing import Dict
from config_data.config import RAPID_API_KEY

def _super_request(end_point: str, method: str, params: dict):
	url = "https://hotels4.p.rapidapi.com" + end_point
	if method == 'GET':
		return _get_request(url=url, params=params)

	if method == 'POST':
		return _post_request(url=url, params=params)

def _get_request(url, params):
	headers = {
		"X-RapidAPI-Key": RAPID_API_KEY,
		"X-RapidAPI-Host": "hotels4.p.rapidapi.com"
	}
	response = requests.request("GET", url, headers=headers, params=params, timeout=15)
	print(url, 'get request')
	if response.status_code == 200:
		return response.json()


def _post_request(url: str, params: Dict):
	headers = {
		"content-type": "application/json",
		"X-RapidAPI-Key": RAPID_API_KEY,
		"X-RapidAPI-Host": "hotels4.p.rapidapi.com"
	}
	response = requests.request("POST", url, json=params, headers=headers, timeout=15)
	print(url, 'post request')

	if response.status_code == 200:
		return response.json()

class ApiInterface():
	@staticmethod
	def super_request():
		return _super_request




