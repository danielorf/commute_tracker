from flask import Flask, jsonify, abort, make_response, request, url_for, render_template
from datetime import datetime, timedelta
import pymysql
from helper_functions import date_formatter

# app = Flask(__name__)
#
# @app.errorhandler(404)
# def not_found(error):
#     return make_response(jsonify({'error': 'Not found'}), 404)

conn = pymysql.connect(host='192.168.100.3', port=32776, user='admin', passwd='oYwU50bjQ4Et', db='commute')
cur = conn.cursor()

cur.execute("select * from commute order by id desc limit 1000")

date_list = []
min_to_red_list = []
min_to_home_list = []

#print(cur.fetchone())

for row in cur:
    year = date_formatter(row[1])
    month = date_formatter(row[2])
    day = date_formatter(row[3])
    hour = date_formatter(row[5])
    minute = date_formatter(row[6])
    date = '{}-{}-{} {}:{}'.format(year,month,day,hour,minute)
    date_list.append(date)
    min_to_red_list.append(round(float(row[7])/60,2))
    min_to_home_list.append(round(float(row[8])/60,2))


print(date_list)
print(min_to_red_list)
print(min_to_home_list)

cur.close()
conn.close()





# n_days_ago = 100
# date_at_n_days_ago = datetime.now() - timedelta(days=n_days_ago)
# # sec_list = ['TSLA', 'MMM', 'SLB', 'WFC', 'DIS', 'AAPL', 'MSFT', 'BA', 'JWN', 'CG', 'HBI']
# sec_name1 = 'BA'
# sec_name2 = 'TSLA'
# security1 = Share(sec_name1)
# security2 = Share(sec_name2)
# sec_hist1 = security1.get_historical(str(date_at_n_days_ago.date()), str(datetime.now().date()))
# sec_hist2 = security2.get_historical(str(date_at_n_days_ago.date()), str(datetime.now().date()))
#
# date_list1 = []
# close_list1 = []
# date_list2 = []
# close_list2 = []
#
# for a in sec_hist1:
#     date_list1.append(a['Date'])
#     close_list1.append(float(a['Close']))
#
# for b in sec_hist2:
#     date_list2.append(b['Date'])
#     close_list2.append(float(b['Close']))
#
# @app.route('/plotly_line_stock/', methods=['GET'])
# def get_plotly_line_stock():
#     print('plotly_line_stock')
#     #print(date_list)
#     print(close_list1)
#     print(close_list2)
#     return render_template('plotly_line_stock.html', sec_name1=sec_name1,
#     plot_data_date1=date_list1, plot_data_close1=close_list1, sec_name2=sec_name2,
#     plot_data_date2=date_list2, plot_data_close2=close_list2)
#
# @app.route('/plotly_line_stock2/', methods=['GET'])
# def get_plotly_line_stock2():
#     print('plotly_line_stock2')
#     return render_template('plotly_line_stock2.html')
#
# @app.route('/plotly_finance/', methods=['GET'])
# def get_plotly_finance():
#     print('plotly_finanace')
#     return render_template('plotly_finance.html')
#
#
# if __name__ == '__main__':
#     app.run(debug=True)
