from surch.V3_SEARCH import LocationID
from surch.V2_LIST import HotelsID


create_json_with_location_id = LocationID.set_city()
create_json_with_location_id('Рига', 'ru-RU')

get_location_id = LocationID.get_id()
id = get_location_id()

create_json_with_hotels_propertys = HotelsID.set_propertys()
create_json_with_hotels_propertys(id[0], adults=1, min_price=50, max_price=125)

hotels_list = HotelsID.get_hotels_list()
hotels_list = hotels_list()


print('ID города {}. название {}'.format(id[0], id[1]))
for string in hotels_list:
    print(string)