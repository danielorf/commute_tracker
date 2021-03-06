import googlemaps, datetime, time
import pymysql
import tokens_and_addresses
import pytz


def get_fastest_transit(directions_object_list, now_epoch):
    """
    Returns fastest bus route and time based on current time

    :param directions_object_list: List of Google Maps Directions objects each containing
    transit directions between source and destination
    :type directions_object_list: List of Google Maps Directions objects
    """
    fastest_dir = directions_object_list[0]
    fastest_dir_time = (directions_object_list[0]['legs'][0]['arrival_time']['value'] - now_epoch) / 60
    for dirobj in directions_object_list:
        temp_dir_time = (dirobj['legs'][0]['arrival_time']['value'] - now_epoch) / 60
        if temp_dir_time < fastest_dir_time:
            fastest_dir = dirobj
            fastest_dir_time = temp_dir_time

    fastest_dir_steps = fastest_dir['legs'][0]['steps']
    primary_step = fastest_dir_steps[0]
    primary_step_time = 0
    for step in fastest_dir_steps:
        if step['travel_mode'] == 'TRANSIT':
            temp_step_time = int(step['duration']['value'])
            if temp_step_time > primary_step_time:
                primary_step = step
                primary_step_time = temp_step_time

    fastest_bus_route = primary_step['transit_details']['line']['short_name']

    return fastest_bus_route, round(fastest_dir_time, 1)


directions_api_key = tokens_and_addresses.google_maps_directions_api_key

gmaps = googlemaps.Client(key=directions_api_key)

home = tokens_and_addresses.home_coords
downtown = tokens_and_addresses.downtown_coords
mukilteo = tokens_and_addresses.mukilteo_coords

db = pymysql.connect(host=tokens_and_addresses.sql_host, port=tokens_and_addresses.sql_port,
                     user=tokens_and_addresses.sql_username, passwd=tokens_and_addresses.sql_password,
                     db='commute2')
cursor = db.cursor()
sql = """CREATE TABLE IF NOT EXISTS commute2 (
    id INT PRIMARY KEY AUTO_INCREMENT,
    epoch_time INT,
    year SMALLINT,
    month TINYINT,
    day TINYINT,
    day_code TINYINT,
    hour TINYINT,
    minute TINYINT,
    time_home2downtown FLOAT,
    time_downtown2home FLOAT,
    time_home2downtownbus FLOAT,
    route_home2downtownbus VARCHAR(7),
    time_downtown2homebus FLOAT,
    route_downtown2homebus VARCHAR(7),
    time_home2mukilteo FLOAT,
    time_mukilteo2home FLOAT)"""

cursor.execute(sql)
db.close()

while True:
    db = pymysql.connect(host=tokens_and_addresses.sql_host, port=tokens_and_addresses.sql_port,
                         user=tokens_and_addresses.sql_username, passwd=tokens_and_addresses.sql_password,
                         db='commute2')
    cursor = db.cursor()
    try:
        now_epoch = int(time.time())
        now_object = datetime.datetime
        now = now_object.now()

        timezone = pytz.timezone("America/Los_Angeles")
        now_local = timezone.localize(now)

        year = int(now_local.year)
        month = int(now_local.month)
        day = int(now_local.day)
        hour = int(now_local.hour)
        minute = int(now_local.minute)
        day_code = int(now_local.today().weekday())

        print(now_local)

        dir_driving_home_to_downtown = gmaps.directions(home, downtown, departure_time=now_local)
        dir_driving_downtown_to_home = gmaps.directions(downtown, home, departure_time=now_local)
        dir_transit_home_to_downtown = gmaps.directions(home, downtown, departure_time=now_local, mode='transit',
                                                        transit_mode='bus', alternatives=True)
        dir_transit_downtown_to_home = gmaps.directions(downtown, home, departure_time=now_local, mode='transit',
                                                        transit_mode='bus', alternatives=True)
        dir_driving_home_to_mukilteo = gmaps.directions(home, mukilteo, departure_time=now_local)
        dir_driving_mukilteo_to_home = gmaps.directions(mukilteo, home, departure_time=now_local)

        route_home2downtownbus, time_home2downtownbus = get_fastest_transit(dir_transit_home_to_downtown, now_epoch)
        route_downtown2homebus, time_downtown2homebus = get_fastest_transit(dir_transit_downtown_to_home, now_epoch)

        time_driving_home_to_downtown = round(dir_driving_home_to_downtown[0]['legs'][0]['duration_in_traffic']['value'] / 60, 1)
        time_driving_downtown_to_home = round(dir_driving_downtown_to_home[0]['legs'][0]['duration_in_traffic']['value'] / 60, 1)
        time_driving_home_to_mukilteo = round(dir_driving_home_to_mukilteo[0]['legs'][0]['duration_in_traffic']['value'] / 60, 1)
        time_driving_mukilteo_to_home = round(dir_driving_mukilteo_to_home[0]['legs'][0]['duration_in_traffic']['value'] / 60, 1)


    except KeyError as e1:
        print('KeyError, missing dictionary key: ', e1)
        time.sleep(30)
        continue

    sql2 = "INSERT INTO commute2 (epoch_time, year, month, day, day_code, hour, minute, time_home2downtown, " \
           "time_downtown2home, time_home2downtownbus, route_home2downtownbus, time_downtown2homebus, " \
           "route_downtown2homebus, time_home2mukilteo, time_mukilteo2home) " \
           "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(sql2, (now_epoch, year, month, day, day_code, hour, minute, time_driving_home_to_downtown,
                          time_driving_downtown_to_home, time_home2downtownbus, route_home2downtownbus,
                          time_downtown2homebus, route_downtown2homebus, time_driving_home_to_mukilteo,
                          time_driving_mukilteo_to_home))
    db.commit()
    print("committed to db @ {}".format(datetime.datetime.now()))
    db.close()
    print("closed db connection")
    time.sleep(300)  # Wait 5 min before next collecting commute data again
