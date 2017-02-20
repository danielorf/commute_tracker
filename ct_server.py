from flask import Flask, jsonify, make_response, render_template
from helper_functions import get_commute_data, get_commute_data_by_day
from testing_data import test_date_list, test_time_to_red_list, test_time_to_home_list
from commute import Commute
import time

app = Flask(__name__)

# Testing data switch
use_testing_data = False


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/commute/', methods=['GET'])
def get_commute_plot():
    # if use_testing_data:
    #     date_list = test_date_list
    #     min_to_red_list = test_time_to_red_list
    #     min_to_home_list = test_time_to_home_list
    # else:

    start_time = time.time()

    commute = Commute()
    commute.get_commute_data(5000)

    print('Total time: ', time.time() - start_time)

    return render_template('commute.html',
                           plot_to_red_name='time 2 mukilteo',
                           plot_to_home_name='time 2 home',
                           plot_data_date=commute.date_list,
                           plot_data_min2red=commute.drive_time_home2mukilteo_list,
                           plot_data_min2home=commute.drive_time_mukilteo2home_list)

@app.route('/commute/<int:num>', methods=['GET'])
def get_commute_plot_num(num):
    # if use_testing_data:
    #     date_list = test_date_list
    #     min_to_red_list = test_time_to_red_list
    #     min_to_home_list = test_time_to_home_list
    # else:
    #     date_list, min_to_red_list, min_to_home_list = get_commute_data(num)

    commute = Commute()
    commute.get_commute_data(num)

    return render_template('commute.html',
                           plot_to_red_name='time 2 downtown',
                           plot_to_home_name='time 2 home',
                           plot_data_date=commute.date_list,
                           plot_data_min2red=commute.drive_time_home2downtown_list,
                           plot_data_min2home=commute.drive_time_downtown2home_list)


@app.route('/commute_day/<int:day_code>', methods=['GET'])
def get_commute_plot_by_day(day_code):
    # if use_testing_data:
    #     date_list = test_date_list
    #     min_to_red_list = test_time_to_red_list
    #     min_to_home_list = test_time_to_home_list
    # else:

    commute = Commute()
    commute.get_commute_data_by_day(1000, day_code)

    return render_template('commute.html',
                           plot_to_red_name='time 2 muk',
                           plot_to_home_name='time 2 home',
                           plot_data_date=commute.date_list,
                           plot_data_min2red=commute.drive_time_home2mukilteo_list,
                           plot_data_min2home=commute.drive_time_mukilteo2home_list)

if __name__ == '__main__':
    app.run(debug=True,
            host='0.0.0.0'
            )
