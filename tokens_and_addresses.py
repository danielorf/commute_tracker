‘’’
Fill in details for ‘sql_host’, ‘sql_username’, ’sql_password’, ‘google_maps_directions_api_key’, and ‘home_coords’
‘’’


sql_host = ''
sql_port = 3306  # 3306 is default for MySql
sql_username = '’
sql_password = ''

google_maps_directions_api_key = ''

home_coords = ''  # In the form of 'Lat, Lon'
downtown_coords = '47.609875, -122.337941'  # In the form of 'Lat, Lon'
mukilteo_coords = '47.896056, -122.297405'  # In the form of 'Lat, Lon'

db_column_list_from_home = ['time_home2downtown', 'time_home2mukilteo']
db_column_list_to_home = ['time_downtown2home', 'time_mukilteo2home']
location_list = ['Downtown', 'Mukilteo']
