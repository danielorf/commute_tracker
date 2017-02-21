from flask import Flask, jsonify, make_response, render_template
from helper_functions import get_commute_data, get_commute_data_by_day
from testing_data import test_date_list, test_time_to_red_list, test_time_to_home_list
import tokens_and_addresses
from commute import Commute
import time

app = Flask(__name__)

# Testing data switch
use_testing_data = False

db_column_list_from_home = tokens_and_addresses.db_column_list_from_home
db_column_list_to_home = tokens_and_addresses.db_column_list_to_home


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/default/', methods=['GET'])
def get_default_commute_plot():
    # if use_testing_data:
    #     date_list = test_date_list
    #     min_to_red_list = test_time_to_red_list
    #     min_to_home_list = test_time_to_home_list
    # else:

    start_time = time.time()

    downtown_commute = Commute('time_home2downtown', 'time_downtown2home')
    downtown_commute.get_commute_data(5000)

    print('Total time: ', time.time() - start_time)

    return render_template('commute.html',
                           plot_to_red_name='time 2 downtown',
                           plot_to_home_name='time 2 home',
                           plot_data_date=downtown_commute.date_list,
                           plot_data_min2red=downtown_commute.drive_time_from_home_list,
                           plot_data_min2home=downtown_commute.drive_time_to_home_list)

@app.route('/commute/<dest>', methods=['GET'])
def get_commute_plot(dest):
    for column in db_column_list_from_home:
        if dest in column:
            from_home_db_column = column

    for column in db_column_list_to_home:
        if dest in column:
            to_home_db_column = column

    from_home_commute_name = from_home_db_column
    to_home_commute_name = to_home_db_column

    start_time = time.time()

    commute = Commute(from_home_db_column, to_home_db_column)
    commute.get_commute_data(5000)

    print('Total time: ', time.time() - start_time)

    return render_template('commute.html',
                           plot_to_red_name=from_home_commute_name,
                           plot_to_home_name=to_home_commute_name,
                           plot_data_date=commute.date_list,
                           plot_data_min2red=commute.drive_time_from_home_list,
                           plot_data_min2home=commute.drive_time_to_home_list)

@app.route('/commute/<dest>/<int:num>', methods=['GET'])
def get_commute_plot_num(dest, num):
    for column in db_column_list_from_home:
        if dest in column:
            from_home_db_column = column

    for column in db_column_list_to_home:
        if dest in column:
            to_home_db_column = column

    from_home_commute_name = from_home_db_column
    to_home_commute_name = to_home_db_column

    start_time = time.time()

    commute = Commute(from_home_db_column, to_home_db_column)
    commute.get_commute_data(num)

    print('Total time: ', time.time() - start_time)

    return render_template('commute.html',
                           plot_to_red_name=from_home_commute_name,
                           plot_to_home_name=to_home_commute_name,
                           plot_data_date=commute.date_list,
                           plot_data_min2red=commute.drive_time_from_home_list,
                           plot_data_min2home=commute.drive_time_to_home_list)


@app.route('/commute_day/<dest>/<int:day_code>', methods=['GET'])
def get_commute_plot_by_day(dest, day_code):
    # if use_testing_data:
    #     date_list = test_date_list
    #     min_to_red_list = test_time_to_red_list
    #     min_to_home_list = test_time_to_home_list
    # else:

    for column in db_column_list_from_home:
        if dest in column:
            from_home_db_column = column

    for column in db_column_list_to_home:
        if dest in column:
            to_home_db_column = column

    from_home_commute_name = from_home_db_column
    to_home_commute_name = to_home_db_column

    start_time = time.time()

    commute = Commute(from_home_db_column, to_home_db_column)
    # downtown_commute.get_commute_data(num)
    commute.get_commute_data_by_day(1000, day_code)

    print('Total time: ', time.time() - start_time)

    return render_template('commute.html',
                           plot_to_red_name=from_home_commute_name,
                           plot_to_home_name=to_home_commute_name,
                           plot_data_date=commute.date_list,
                           plot_data_min2red=commute.drive_time_from_home_list,
                           plot_data_min2home=commute.drive_time_to_home_list)

if __name__ == '__main__':
    app.run(debug=True,
            host='0.0.0.0'
            )
