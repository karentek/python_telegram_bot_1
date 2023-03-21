from surch.V3_SEARCH import LocationID


make_json_with_location_id = LocationID.request_location()
make_json_with_location_id('Рига', 'ru-RU')


get_location_id = LocationID.find_location_id()
ids = get_location_id()

print('ID города {}. название {}'.format(ids[0], ids[1]))