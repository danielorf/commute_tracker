import pymysql

conn = pymysql.connect(host='192.168.100.3', port=32776, user='admin', passwd='oYwU50bjQ4Et', db='commute')

cur = conn.cursor()
#cur.execute("SELECT * FROM archive")
cur.execute("select * from commute order by id desc limit 100")

print(cur.description)
print()

#print(cur.fetchall()[0])

for row in cur:
    print(row)

cur.close()
conn.close()