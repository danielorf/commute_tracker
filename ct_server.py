from flask import Flask, jsonify, make_response, render_template
from helper_functions import get_commute_data, get_commute_data_by_day

app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/commute/', methods=['GET'])
def get_commute_plot():
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
    date_list, min_to_red_list, min_to_home_list = get_commute_data(num)
    print(date_list)
    print(min_to_red_list)
    return render_template('commute.html',
                           plot_to_red_name='time 2 red',
                           plot_to_home_name='time 2 home',
                           plot_data_date=date_list,
                           plot_data_min2red=min_to_red_list,
                           plot_data_min2home=min_to_home_list)

#date_list = ['02:34', '03:56', '05:06']
#min_to_red_list = [1.00, 2.00, 3.00]
#min_to_home_list = [2.00, 3.00, 5.00]

@app.route('/commute_day/<int:day_code>', methods=['GET'])
def get_commute_plot_by_day(day_code):
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
    app.run(debug=True)
