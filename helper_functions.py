import pymysql

# Auto formats date values (month, day, hour, minute) to two digits - needed for proper date formatting by Plotly
def date_formatter(val):
    if val < 10:
        val = '{}{}'.format('0', str(val))
        return val
    elif val >= 10:
        return str(val)
    else:
        print('Improper date value formatting')
        print(val)


def get_commute_data():
    conn = pymysql.connect(host='192.168.100.3', port=32776, user='admin', passwd='oYwU50bjQ4Et', db='commute')
    cur = conn.cursor()

    cur.execute("select * from commute order by id desc limit 1000")

    date_list = []
    id_list = []
    min_to_red_list = []
    min_to_home_list = []

    for row in cur:
        year = date_formatter(row[1])
        month = date_formatter(row[2])
        day = date_formatter(row[3])
        hour = date_formatter(row[5])
        minute = date_formatter(row[6])
        date = '{}-{}-{} {}:{}'.format(year, month, day, hour, minute)
        date_list.append(date)
        id_list.append(row[0])
        min_to_red_list.append(round(float(row[7]) / 60, 2))
        min_to_home_list.append(round(float(row[8]) / 60, 2))

    cur.close()
    conn.close()

    return date_list, min_to_red_list, min_to_home_list

