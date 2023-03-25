from surch.hotels_by_city import LocationID
from surch.hotels_list import HotelsID


create_json_with_location_id = LocationID.set_city()
create_json_with_location_id('Рига', 'ru-RU')

get_location_id = LocationID.get_id()
id = get_location_id()


create_json_with_hotels_propertys = HotelsID.set_propertys()
create_json_with_hotels_propertys('3000', adults=7, min_price=50, max_price=125)

hotels_list = HotelsID.get_hotels_list()
hotels_list = hotels_list()


print('ID города {}. название {}'.format(id[0], id[1]))
for string in hotels_list:
    print(string)