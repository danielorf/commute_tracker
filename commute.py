import pymysql, tokens_and_addresses, time
from pandas.io import sql


class Commute:
    """
    Returns lists of dates and associated commute times between two locations

    Attributes:
        date_list                    List of date/time for particular commute time records.
        drive_time_from_home_list    List of commute times from home to destination.
        drive_time_to_home_list      List of commute times from destination to home.
    """
    date_list = []
    drive_time_from_home_list = []
    drive_time_to_home_list = []

    def __init__(self, from_home_db_column, to_home_db_column):
        """
        :param from_home_db_column: Name of database column containing commute times from
         home to a destination
        :type from_home_db_column: string

        :param to_home_db_column: Name of database column containing commute times from
         a destination to home.
        :type to_home_db_column: string
        """
        self.from_home_db_column = from_home_db_column
        self.to_home_db_column = to_home_db_column

    def get_commute_data(self, num_records):
        """
        Retrieves commute data from database and assigns data to date_list, drive_time_from_home_list
        and drive_time_to_home_list.

        :param num_records: Number of database records to return
        :type num_records: int
        """
        conn = pymysql.connect(host=tokens_and_addresses.sql_host, port=tokens_and_addresses.sql_port,
                               user=tokens_and_addresses.sql_username, passwd=tokens_and_addresses.sql_password,
                               db='commute2')

        query = "select * from commute2 order by id desc limit {}".format(str(num_records))
        commute_df = sql.read_sql_query(query, con=conn)

        start_time = time.time()

        date_list = []
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
        '''
        Retrieves commute data for a particular day of the week or class of day (weekday/weekend)
        from database and assigns data to date_list, drive_time_from_home_list
        and drive_time_to_home_list.

        day code explanation:  0:Monday-6:Sunday, 7:AllDays, 8:OnlyWeekdays, 9:OnlyWeekends

        :param num_records: Number of database records to return
        :type num_records: int

        :param day_code: Code for a particular day of the week or class of day (weekday/weekend)
        with the following format: 0:Monday-6:Sunday, 7:AllDays, 8:OnlyWeekdays, 9:OnlyWeekends
        :type day_code: int
        '''

        conn = pymysql.connect(host=tokens_and_addresses.sql_host, port=tokens_and_addresses.sql_port,
                               user=tokens_and_addresses.sql_username, passwd=tokens_and_addresses.sql_password,
                               db='commute2')

        if (day_code >= 0 and day_code <= 6):
            query = "select * from commute2 " \
                    "where day_code={} " \
                    "order by hour asc, minute asc " \
                    "limit {}".format(day_code, str(num_records))

        elif (day_code == 7):
            query = "select * from commute2 "\
                        "order by hour asc, minute asc " \
                        "limit {}".format(str(num_records))

        elif (day_code == 8):
            query = "select * from commute2 " \
                        "where not (day_code=5 or day_code=6) " \
                        "order by hour desc, minute desc " \
                        "limit {}".format(str(num_records))

        elif (day_code == 9):
            query = "select * from commute2 " \
                        "where day_code=5 or day_code=6 " \
                        "order by hour asc, minute asc " \
                        "limit {}".format(str(num_records))

        commute_df = sql.read_sql(query, con=conn)

        start_time = time.time()

        self.drive_time_from_home_list = commute_df[self.from_home_db_column].tolist()
        self.drive_time_to_home_list = commute_df[self.to_home_db_column].tolist()

        date_list = []

        for row in commute_df.itertuples():
            hour = date_formatter(row.hour)
            minute = date_formatter(row.minute)
            date = '{}:{}'.format(hour, minute)
            date_list.append(date)

        self.date_list = date_list

        print('Total time: ', time.time() - start_time)

        conn.close()


def date_formatter(date_val):
    """
    Auto formats date values (month, day, hour, minute) to two digits.  This is needed for
    proper date formatting by Plotly.
    i.e. the month of March is represented in the database as and integer of 3.  This needs
    to be changed to a string of '03' to be plotted properly.

    :param date_val: Date/time value (month, day, hour, minute, second)
    :type date_val: int
    """
    if date_val < 10:
        date_val = '{}{}'.format('0', str(date_val))
        return date_val
    elif date_val >= 10:
        return str(date_val)
    else:
        print('Improper date value formatting')
        print(date_val)
