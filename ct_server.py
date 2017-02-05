from flask import Flask, jsonify, abort, make_response, request, url_for, render_template
from datetime import datetime, timedelta
import pymysql
from helper_functions import date_formatter
import json

app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

conn = pymysql.connect(host='192.168.100.3', port=32776, user='admin', passwd='oYwU50bjQ4Et', db='commute')
cur = conn.cursor()

cur.execute("select * from commute order by id desc limit 1000")

date_list = []
id_list = []
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
    #date = '{}-{}-{} {}'.format(year, month, day, hour)
    date_list.append(date)
    id_list.append(row[0])
    min_to_red_list.append(round(float(row[7])/60,2))
    min_to_home_list.append(round(float(row[8])/60,2))

# print(date_list)
# print(min_to_red_list)
# print(min_to_home_list)
#print(id_list)

cur.close()
conn.close()

# print(id_list)
# print(type(id_list))
# print(type(id_list[0]))
# print(min_to_red_list)
# print(type(min_to_red_list))
# print(type(min_to_red_list[0]))

#id_list = id_list.reverse()


#date_list = ['2017-02-03', '2017-02-02', '2017-02-01', '2017-01-31', '2017-01-30', '2017-01-27', '2017-01-26', '2017-01-25', '2017-01-24', '2017-01-23', '2017-01-20', '2017-01-19', '2017-01-18', '2017-01-17', '2017-01-13', '2017-01-12', '2017-01-11', '2017-01-10', '2017-01-09', '2017-01-06', '2017-01-05', '2017-01-04', '2017-01-03', '2016-12-30', '2016-12-29', '2016-12-28', '2016-12-27', '2016-12-23', '2016-12-22', '2016-12-21', '2016-12-20', '2016-12-19', '2016-12-16', '2016-12-15', '2016-12-14', '2016-12-13', '2016-12-12', '2016-12-09', '2016-12-08', '2016-12-07', '2016-12-06', '2016-12-05', '2016-12-02', '2016-12-01', '2016-11-30', '2016-11-29', '2016-11-28', '2016-11-25', '2016-11-23', '2016-11-22', '2016-11-21', '2016-11-18', '2016-11-17', '2016-11-16', '2016-11-15', '2016-11-14', '2016-11-11', '2016-11-10', '2016-11-09', '2016-11-08', '2016-11-07', '2016-11-04', '2016-11-03', '2016-11-02', '2016-11-01', '2016-10-31', '2016-10-28']
#min_to_red_list = [162.399994, 162.259995, 163.970001, 163.419998, 165.570007, 167.699997, 169.119995, 167.360001, 160.550003, 157.839996, 159.529999, 159.0, 158.320007, 157.669998, 158.830002, 158.289993, 159.399994, 159.070007, 158.320007, 159.100006, 158.710007, 158.619995, 156.970001, 155.679993, 155.690002, 156.100006, 157.479996, 157.809998, 157.460007, 157.479996, 156.389999, 156.179993, 154.5, 153.770004, 154.470001, 156.660004, 157.160004, 156.490005, 155.389999, 154.139999, 152.240005, 152.160004, 152.25, 152.389999, 150.559998, 151.639999, 149.770004, 150.039993, 149.740005, 149.520004, 147.020004, 146.350006, 145.330002, 146.440002, 148.110001, 149.990005, 148.520004, 147.690002, 145.089996, 142.199997, 143.029999, 139.539993, 140.020004, 140.75, 142.410004, 142.429993, 143.009995]


@app.route('/commute/', methods=['GET'])
def get_commute_plot():
    # print('plotly_line_stock')
    print(date_list)
    # print(close_list1)
    # print(close_list2)
    # print(id_list)
    # print(type(id[0]))
    print(min_to_red_list)
    # print(type(min_to_red_list[0]))
    return render_template('commute.html',
                           plot_data_date=date_list,
                           plot_data_min2red=min_to_red_list,)



if __name__ == '__main__':
    app.run(debug=True)
