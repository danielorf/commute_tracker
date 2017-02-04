import pymysql

conn = pymysql.connect(host='192.168.100.3', port=32776, user='admin', passwd='oYwU50bjQ4Et', db='weewx')

cur = conn.cursor()
#cur.execute("SELECT * FROM archive")
cur.execute("select * from archive order by dateTime desc limit 1000")

print(cur.description)
print()

for row in cur:
    print(row)

cur.close()
conn.close()