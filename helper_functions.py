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


def get_commute_data(num_records):
    conn = pymysql.connect(host='192.168.100.3', port=32776, user='admin', passwd='oYwU50bjQ4Et', db='commute')
    cur = conn.cursor()

    cur.execute("select * from commute order by id desc limit {}".format(str(num_records)))

    date_list = []
    #id_list = []
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
        #id_list.append(row[0])
        min_to_red_list.append(round(float(row[7]) / 60, 2))
        min_to_home_list.append(round(float(row[8]) / 60, 2))

    cur.close()
    conn.close()

    return date_list, min_to_red_list, min_to_home_list

def get_commute_data_by_day(num_records, day_code):
    '''day code explanation:
    0:Monday-6:Sunday, 7:AllDays, 8:OnlyWeekdays, 9:OnlyWeekends
    '''
    conn = pymysql.connect(host='192.168.100.3', port=32776, user='admin', passwd='oYwU50bjQ4Et', db='commute')
    cur = conn.cursor()

    if (day_code >= 0 and day_code <= 6):
        cur.execute("select * from commute "
                    "where day_code={} "
                    #"order by hour asc, minute asc "
                    "limit {}".format(day_code, str(num_records)))
    elif (day_code == 7):
        cur.execute("select * from commute "
                    #"where day_code={} "
                    # "order by hour asc, minute asc "
                    "limit {}".format(str(num_records)))
    elif (day_code == 8):
        cur.execute("select * from commute "
                    "where not (day_code=5 or day_code=6) "
                    "order by hour asc, minute asc "
                    "limit {}".format(str(num_records)))
    elif (day_code == 9):
        cur.execute("select * from commute "
                    "where day_code=5 or day_code=6 "
                    "order by hour asc, minute asc "
                    "limit {}".format(str(num_records)))

    date_list = []
    min_to_red_list = []
    min_to_home_list = []

    for row in cur:
        hour = date_formatter(row[5])
        minute = date_formatter(row[6])
        date = '{}:{}'.format(hour, minute)
        date_list.append(date)
        min_to_red_list.append(round(float(row[7]) / 60, 2))
        min_to_home_list.append(round(float(row[8]) / 60, 2))

    cur.close()
    conn.close()

    return date_list, min_to_red_list, min_to_home_list

def get_fastest_transit(directions_object_array, now_epoch):
    fastest_dir = directions_object_array[0]
    fastest_dir_time = (directions_object_array[0]['legs'][0]['arrival_time']['value'] - now_epoch) / 60
    for dirobj in directions_object_array:
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