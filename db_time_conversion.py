# Used to convert UTC times in database to local time

import pymysql
import tokens_and_addresses
import datetime

db = pymysql.connect(host=tokens_and_addresses.sql_host, port=tokens_and_addresses.sql_port,
                     user=tokens_and_addresses.sql_username, passwd=tokens_and_addresses.sql_password,
                     db='commute2')

cursor = db.cursor()

sql = "SELECT epoch_time from commute2"
cursor.execute(sql)
timestamps = cursor.fetchall()
timestamps = [stamp[0] for stamp in timestamps]

print(timestamps[-1])
print(datetime.datetime.fromtimestamp(timestamps[-1]))
print(datetime.datetime.fromtimestamp(timestamps[-1]).hour)
print(datetime.datetime.fromtimestamp(timestamps[-1]).weekday())

new_sql = "UPDATE test SET value=0 WHERE test_id IN(1, 2, 3)"

new_sql = """
UPDATE commute2
   SET year=%s, month=%s, day=%s, day_code=%s, hour=%s
   WHERE epoch_time=%s
"""
    #(year, month, day, day_code, hour, epoch_time)


for time in timestamps:
    updated_time = datetime.datetime.fromtimestamp(time)
    new_times = (int(updated_time.year), int(updated_time.month), int(updated_time.day), int(updated_time.weekday()), int(updated_time.hour), int(time))
    cursor.execute(new_sql,new_times)

db.commit()
db.close()
print('success')
#print('success')

