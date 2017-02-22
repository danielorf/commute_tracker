Description: Commute tracking application written in python 3.5, flask, MySql, javascript, html and css (Bootstrap).  This application gathers commute times using Google Maps at 5 minute intervals using 'data_collection.py'.  A flask server (using 'ct_server.py') is used to display the data in a web page with the help of Bootstrap and Plotly. Data can be displayed with a history of up to 10 days.  It can also be broken down per day of the week as well as all weekdays and weekends.

'tokens_and_addresses.py' must be filled out with MySQL server login details, Google Maps API key, location data, and location names list before data collection and webserver can function.

Installation requirements listed in 'requirements.txt'.