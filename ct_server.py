from flask import Flask, jsonify, make_response, render_template
import tokens_and_addresses
from commute import Commute
import time

app = Flask(__name__)

db_column_list_from_home = tokens_and_addresses.db_column_list_from_home
db_column_list_to_home = tokens_and_addresses.db_column_list_to_home
location = tokens_and_addresses.location_list[0]  # Default to first on list


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/default/', methods=['GET'])
def get_default_commute_plot():
    start_time = time.time()
    global location
    dest = location.lower()
    for column in db_column_list_from_home:
        if dest in column:
            from_home_db_column = column

    for column in db_column_list_to_home:
        if dest in column:
            to_home_db_column = column


    commute = Commute(from_home_db_column, to_home_db_column)
    commute.get_commute_data(2500)

    processing_time = time.time() - start_time
    processing_time_string = '{}{}'.format(round(processing_time, 2), ' seconds ')

    return render_template('commute.html',
                           processing_time=processing_time_string,
                           show_markers=False,
                           use_error_bars=False,
                           location=location,
                           plot_from_home_name='time to ' + location,
                           plot_to_home_name='time to Home',
                           plot_data_date=commute.date_list,
                           plot_data_from_home=commute.drive_time_from_home_list,
                           plot_data_to_home=commute.drive_time_to_home_list,
                           plot_data_stdev_from_home=[],
                           plot_data_stdev_to_home=[]
                           )

@app.route('/commute/<dest>', methods=['GET'])
def get_commute_plot(dest):
    start_time = time.time()
    dest = dest.lower()
    for column in db_column_list_from_home:
        if dest in column:
            from_home_db_column = column

    for column in db_column_list_to_home:
        if dest in column:
            to_home_db_column = column


    commute = Commute(from_home_db_column, to_home_db_column)
    commute.get_commute_data(5000)

    processing_time = time.time() - start_time
    processing_time_string = '{}{}'.format(round(processing_time, 2), ' seconds ')

    return render_template('commute.html',
                           processing_time=processing_time_string,
                           show_markers=True,
                           use_error_bars=False,
                           location=location,
                           plot_from_home_name='time to '+location,
                           plot_to_home_name='time to Home',
                           plot_data_date=commute.date_list,
                           plot_data_from_home=commute.drive_time_from_home_list,
                           plot_data_to_home=commute.drive_time_to_home_list,
                           plot_data_stdev_from_home=[],
                           plot_data_stdev_to_home=[]
                           )

@app.route('/commute/<dest>/<int:num>', methods=['GET'])
def get_commute_plot_num(dest, num):
    start_time = time.time()
    dest = dest.lower()
    for column in db_column_list_from_home:
        if dest in column:
            from_home_db_column = column

    for column in db_column_list_to_home:
        if dest in column:
            to_home_db_column = column


    commute = Commute(from_home_db_column, to_home_db_column)
    commute.get_commute_data(num)

    processing_time = time.time() - start_time
    processing_time_string = '{}{}'.format(round(processing_time, 2), ' seconds ')

    return render_template('commute.html',
                           processing_time=processing_time_string,
                           show_markers=False,
                           use_error_bars=False,
                           location=location,
                           plot_from_home_name='time to '+location,
                           plot_to_home_name='time to Home',
                           plot_data_date=commute.date_list,
                           plot_data_from_home=commute.drive_time_from_home_list,
                           plot_data_to_home=commute.drive_time_to_home_list,
                           plot_data_stdev_from_home=[],
                           plot_data_stdev_to_home=[]
                           )


@app.route('/commute_day/<dest>/<int:day_code>', methods=['GET'])
def get_commute_plot_by_day(dest, day_code):
    start_time = time.time()
    dest = dest.lower()
    for column in db_column_list_from_home:
        if dest in column:
            from_home_db_column = column

    for column in db_column_list_to_home:
        if dest in column:
            to_home_db_column = column

    commute = Commute(from_home_db_column, to_home_db_column)
    commute.get_commute_data_by_day(2016, day_code)  # data collected at 5min rate, 2016 samples per week

    processing_time = time.time() - start_time
    processing_time_string = '{}{}'.format(round(processing_time, 2), ' seconds ')

    return render_template('commute.html',
                           processing_time=processing_time_string,
                           show_markers=False,
                           use_error_bars=False,
                           location=location,
                           plot_from_home_name='time to '+location,
                           plot_to_home_name='time to Home',
                           plot_data_date=commute.date_list,
                           plot_data_from_home=commute.drive_time_from_home_list,
                           plot_data_to_home=commute.drive_time_to_home_list,
                           plot_data_stdev_from_home=[],
                           plot_data_stdev_to_home=[]
                           )

@app.route('/commute_day_avg/<dest>/<int:day_code>', methods=['GET'])
def get_commute_plot_by_day_avg(dest, day_code):
    start_time = time.time()
    dest = dest.lower()
    for column in db_column_list_from_home:
        if dest in column:
            from_home_db_column = column

    for column in db_column_list_to_home:
        if dest in column:
            to_home_db_column = column

    commute = Commute(from_home_db_column, to_home_db_column)
    commute.get_commute_average(5000, day_code)

    processing_time = time.time() - start_time
    processing_time_string = '{}{}'.format(round(processing_time, 2), ' seconds ')

    return render_template('commute.html',
                           processing_time=processing_time_string,
                           show_markers=False,
                           use_error_bars=True,
                           location=location,
                           plot_from_home_name='time to '+location,
                           plot_to_home_name='time to Home',
                           plot_data_date=commute.date_list,
                           plot_data_from_home=commute.drive_time_avg_from_home_list,
                           plot_data_to_home=commute.drive_time_avg_to_home_list,
                           plot_data_stdev_from_home=commute.drive_time_stdev_from_home_list,
                           plot_data_stdev_to_home=commute.drive_time_stdev_to_home_list
                           )


@app.route('/change_location/<loc>', methods=['GET'])
def change_location(loc):
    global location
    location = loc
    return get_default_commute_plot()


if __name__ == '__main__':
    app.run(debug=True,
            host='0.0.0.0',
            port=8000
            )

