import pymysql, tokens_and_addresses
from pandas.io import sql
import time


class Commute:
    date_list = []
    # drive_time_home2downtown_list = []
    # drive_time_downtown2home_list = []
    # bus_time_home2downtown_list = []
    # bus_route_home2downtown_list = []
    # bus_time_downtown2home_list = []
    # bus_route_downtown2home_list = []
    # drive_time_home2mukilteo_list = []
    # drive_time_mukilteo2home_list = []
    drive_time_from_home_list = []
    drive_time_to_home_list = []

    def __init__(self, from_home_db_column, to_home_db_column):
        self.from_home_db_column = from_home_db_column
        self.to_home_db_column = to_home_db_column

    def get_commute_data(self, num_records):
        conn = pymysql.connect(host=tokens_and_addresses.sql_host, port=tokens_and_addresses.sql_port,
                               user=tokens_and_addresses.sql_username, passwd=tokens_and_addresses.sql_password,
                               db='commute2')

        query = "select * from commute2 order by id desc limit {}".format(str(num_records))
        commute_df = sql.read_sql_query(query, con=conn)

        start_time = time.time()

        date_list = []
        # self.drive_time_home2downtown_list = commute_df['time_home2downtown'].tolist()
        # self.drive_time_downtown2home_list = commute_df['time_downtown2home'].tolist()
        # self.bus_time_home2downtown_list = commute_df['time_home2downtownbus'].tolist()
        # self.bus_route_home2downtown_list = commute_df['route_home2downtownbus'].tolist()
        # self.bus_time_downtown2home_list = commute_df['time_downtown2homebus'].tolist()
        # self.bus_route_downtown2home_list = commute_df['route_downtown2homebus'].tolist()
        # self.drive_time_home2mukilteo_list = commute_df['time_home2mukilteo'].tolist()
        # self.drive_time_mukilteo2home_list = commute_df['time_mukilteo2home'].tolist()
        self.drive_time_from_home_list = commute_df[self.from_home_db_column].tolist()
        self.drive_time_to_home_list = commute_df[self.to_home_db_column].tolist()

        for row in commute_df.itertuples():
            # TODO: Consider pushing date formatting into the data collection portion of project.
            # It will require storing as string though.  Time the current implementation first.
            year = date_formatter(row.year)
            month = date_formatter(row.month)
            day = date_formatter(row.day)
            hour = date_formatter(row.hour)
            minute = date_formatter(row.minute)
            date = '{}-{}-{} {}:{}'.format(year, month, day, hour, minute)
            date_list.append(date)

        self.date_list = date_list

        print('Total time: ', time.time() - start_time)

        conn.close()

    def get_commute_data_by_day(self, num_records, day_code):
        '''day code explanation:
        0:Monday-6:Sunday, 7:AllDays, 8:OnlyWeekdays, 9:OnlyWeekends
        '''
        conn = pymysql.connect(host=tokens_and_addresses.sql_host, port=tokens_and_addresses.sql_port,
                               user=tokens_and_addresses.sql_username, passwd=tokens_and_addresses.sql_password,
                               db='commute2')
        #cur = conn.cursor()

        if (day_code >= 0 and day_code <= 6):
            query = "select * from commute2 " \
                    "where day_code={} " \
                    "order by hour asc, minute asc " \
                    "limit {}".format(day_code, str(num_records))

            # cur.execute("select * from commute "
            #             "where day_code={} "
            #             # "order by hour asc, minute asc "
            #             "limit {}".format(day_code, str(num_records)))

        elif (day_code == 7):
            query = "select * from commute2 "\
                        "order by hour asc, minute asc " \
                        "limit {}".format(str(num_records))

            # cur.execute("select * from commute "
            #             # "where day_code={} "
            #             # "order by hour asc, minute asc "
            #             "limit {}".format(str(num_records)))

        elif (day_code == 8):
            query = "select * from commute2 " \
                        "where not (day_code=5 or day_code=6) " \
                        "order by hour desc, minute desc " \
                        "limit {}".format(str(num_records))

            # cur.execute("select * from commute "
            #             "where not (day_code=5 or day_code=6) "
            #             "order by hour asc, minute asc "
            #             "limit {}".format(str(num_records)))

        elif (day_code == 9):
            query = "select * from commute2 " \
                        "where day_code=5 or day_code=6 " \
                        "order by hour asc, minute asc " \
                        "limit {}".format(str(num_records))

            # cur.execute("select * from commute "
            #             "where day_code=5 or day_code=6 "
            #             "order by hour asc, minute asc "
            #             "limit {}".format(str(num_records)))

        commute_df = sql.read_sql(query, con=conn)

        start_time = time.time()

        self.drive_time_from_home_list = commute_df[self.from_home_db_column].tolist()
        self.drive_time_to_home_list = commute_df[self.to_home_db_column].tolist()

        date_list = []
        # self.drive_time_home2downtown_list = commute_df['time_home2downtown'].tolist()
        # self.drive_time_downtown2home_list = commute_df['time_downtown2home'].tolist()
        # self.bus_time_home2downtown_list = commute_df['time_home2downtownbus'].tolist()
        # self.bus_route_home2downtown_list = commute_df['route_home2downtownbus'].tolist()
        # self.bus_time_downtown2home_list = commute_df['time_downtown2homebus'].tolist()
        # self.bus_route_downtown2home_list = commute_df['route_downtown2homebus'].tolist()
        # self.drive_time_home2mukilteo_list = commute_df['time_home2mukilteo'].tolist()
        # self.drive_time_mukilteo2home_list = commute_df['time_mukilteo2home'].tolist()

        for row in commute_df.itertuples():
            # TODO: Consider pushing date formatting into the data collection portion of project.
            # It will require storing as string though.  Time the current implementation first.
            year = date_formatter(row.year)
            month = date_formatter(row.month)
            day = date_formatter(row.day)
            hour = date_formatter(row.hour)
            minute = date_formatter(row.minute)
            date = '{}-{}-{} {}:{}'.format(year, month, day, hour, minute)
            date_list.append(date)

        self.date_list = date_list

        print('Total time: ', time.time() - start_time)

        #cur.close()
        conn.close()

        #return date_list, min_to_red_list, min_to_home_list


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







