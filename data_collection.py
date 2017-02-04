import googlemaps
import datetime
from googlemaps.directions import directions
import time

#import pymysql


geocode_api_key = 'AIzaSyDGoq8IaQO0CBXlXF7pp20S6_kkon2iWBE'
directions_api_key = 'AIzaSyDf7hiKb7E1JfJki6mBQFZjVAF7LoEEo-Q'

gmaps = googlemaps.Client(key=directions_api_key)


home = '47.725065, -122.359203'
red = '47.689102, -122.149295'


'''
#dir_result = gmaps.directions("4413 Chennault Beach Rd, Mukilteo, WA", "11700 Mukilteo Speedway, Mukilteo, WA")

dir_result = gmaps.directions(home, there, departure_time=datetime.datetime.now())
dir_result_rev = gmaps.directions(there, home, departure_time=datetime.datetime.now())

print(dir_result[0]['legs'][0]['duration'])
print(dir_result_rev[0]['legs'][0]['duration'])
print()
print(dir_result[0]['legs'][0]['duration_in_traffic'])
print(dir_result_rev[0]['legs'][0]['duration_in_traffic'])
'''


#db = pymysql.connect(host='192.168.100.3', port=32769, user='admin', passwd='9ijznW2xjfcg', db='commute')
# db = pymysql.connect(host='192.168.100.3', port=32776, user='admin', passwd='oYwU50bjQ4Et', db='commute')
# cursor = db.cursor()
# sql = """CREATE TABLE IF NOT EXISTS commute (
#     id INT PRIMARY KEY AUTO_INCREMENT,
#     date_time INT,
#     time2red INT,
#     time2home INT)"""
#
# cursor.execute(sql)
# db.close()

while True:
    #db = pymysql.connect(host='192.168.100.3', port=32769, user='admin', passwd='9ijznW2xjfcg', db='commute')
    # db = pymysql.connect(host='192.168.100.3', port=32776, user='admin', passwd='oYwU50bjQ4Et', db='commute')
    # cursor = db.cursor()
    try:
        now = datetime.datetime.now()
        dir2red = gmaps.directions(home, red, departure_time=now)
        dir2home = gmaps.directions(red, home, departure_time=now)
        time2red = dir2red[0]['legs'][0]['duration_in_traffic']
        time2home = dir2home[0]['legs'][0]['duration_in_traffic']

        print(time.time())
        print(now)
        print(now.hour)
        print(datetime.datetime.today().weekday())
        print('Time to red: ', time2red)
        print('Time to home: ', time2home)
        print()

    except KeyError as e1:
        print('KeyError, missing dictionary key: ', e1)
        time.sleep(30)
        continue




    # sql2 = "INSERT INTO `commute` (`date_time`, `time2red`, `time2home`) VALUES (%s, %s, %s)"
    # cursor.execute(sql2, (int(time.time()), int(time2red['value']), int(time2home['value'])))
    # #cursor.execute(sql2, (1, 2, 3))
    # db.commit()
    # print("commited to db")
    # db.close()
    # print("closed db connection")
    time.sleep(150)