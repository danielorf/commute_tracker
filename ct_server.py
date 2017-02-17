from flask import Flask, jsonify, make_response, render_template
from helper_functions import get_commute_data, get_commute_data_by_day
from testing_data import test_date_list, test_time_to_red_list, test_time_to_home_list

app = Flask(__name__)

# Testing data switch
use_testing_data = False


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/commute/', methods=['GET'])
def get_commute_plot():
    if use_testing_data:
        date_list = test_date_list
        min_to_red_list = test_time_to_red_list
        min_to_home_list = test_time_to_home_list
    else:
        date_list, min_to_red_list, min_to_home_list = get_commute_data(5000)

    print(date_list)
    print(min_to_red_list)
    return render_template('commute.html',
                           plot_to_red_name='time 2 red',
                           plot_to_home_name='time 2 home',
                           plot_data_date=date_list,
                           plot_data_min2red=min_to_red_list,
                           plot_data_min2home=min_to_home_list)

@app.route('/commute/<int:num>', methods=['GET'])
def get_commute_plot_num(num):
    if use_testing_data:
        date_list = test_date_list
        min_to_red_list = test_time_to_red_list
        min_to_home_list = test_time_to_home_list
    else:
        date_list, min_to_red_list, min_to_home_list = get_commute_data(num)

    print(date_list)
    print(min_to_red_list)
    return render_template('commute.html',
                           plot_to_red_name='time 2 red',
                           plot_to_home_name='time 2 home',
                           plot_data_date=date_list,
                           plot_data_min2red=min_to_red_list,
                           plot_data_min2home=min_to_home_list)


@app.route('/commute_day/<int:day_code>', methods=['GET'])
def get_commute_plot_by_day(day_code):
    if use_testing_data:
        date_list = test_date_list
        min_to_red_list = test_time_to_red_list
        min_to_home_list = test_time_to_home_list
    else:
        date_list, min_to_red_list, min_to_home_list = get_commute_data_by_day(5000,day_code)

    print(date_list)
    print(min_to_red_list)
    return render_template('commute.html',
                           plot_to_red_name='time 2 red',
                           plot_to_home_name='time 2 home',
                           plot_data_date=date_list,
                           plot_data_min2red=min_to_red_list,
                           plot_data_min2home=min_to_home_list)

if __name__ == '__main__':
    app.run(debug=True,
            host='0.0.0.0'
            )
