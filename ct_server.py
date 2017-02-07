from flask import Flask, jsonify, make_response, render_template
from helper_functions import get_commute_data

app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/commute/', methods=['GET'])
def get_commute_plot():
    date_list, min_to_red_list, min_to_home_list = get_commute_data(1000)
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


if __name__ == '__main__':
    app.run(debug=True)
