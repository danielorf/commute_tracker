import googlemaps
from googlemaps import directions
import datetime
import time

import pymysql


geocode_api_key = 'AIzaSyDGoq8IaQO0CBXlXF7pp20S6_kkon2iWBE'
directions_api_key = 'AIzaSyDf7hiKb7E1JfJki6mBQFZjVAF7LoEEo-Q'

gmaps = googlemaps.Client(key=directions_api_key)


home = '47.725065, -122.359203'
red = '47.689102, -122.149295'


#db = pymysql.connect(host='192.168.100.3', port=32769, user='admin', passwd='9ijznW2xjfcg', db='commute')
db = pymysql.connect(host='192.168.100.3', port=32776, user='admin', passwd='oYwU50bjQ4Et', db='commute')
cursor = db.cursor()
sql = """CREATE TABLE IF NOT EXISTS commute (
    id INT PRIMARY KEY AUTO_INCREMENT,
    year INT,
    month INT,
    day INT,
    day_code INT,
    hour INT,
    minute INT,
    time2red INT,
    time2home INT)"""

cursor.execute(sql)
db.close()

while True:
    #db = pymysql.connect(host='192.168.100.3', port=32769, user='admin', passwd='9ijznW2xjfcg', db='commute')
    db = pymysql.connect(host='192.168.100.3', port=32776, user='admin', passwd='oYwU50bjQ4Et', db='commute')
    cursor = db.cursor()
    try:
        now_object = datetime.datetime
        now = now_object.now()
        dir2red = gmaps.directions(home, red, departure_time=now)
        dir2home = gmaps.directions(red, home, departure_time=now)
        time2red = dir2red[0]['legs'][0]['duration_in_traffic']
        time2home = dir2home[0]['legs'][0]['duration_in_traffic']

        year = int(now.year)
        month = int(now.month)
        day = int(now.day)
        hour = int(now.hour)
        minute = int(now.minute)
        day_code = int(now_object.today().weekday())

        print(year, ' ', month, ' ', day, ' ', hour, ' ', minute)
        print('Time to red: ', time2red)
        print('Time to home: ', time2home)
        print()

    except KeyError as e1:
        print('KeyError, missing dictionary key: ', e1)
        time.sleep(30)
        continue



    sql2 = "INSERT INTO `commute` (`year`, `month`, `day`, `day_code`, `hour`, `minute`, `time2red`, `time2home`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql2, (year, month, day, day_code, hour, minute, int(time2red['value']), int(time2home['value'])))
    db.commit()
    print("commited to db")
    db.close()
    print("closed db connection")
    time.sleep(450)