Description: Commute tracking application written in python 3.5, flask, MySQL, javascript, html and css (Bootstrap).  This application gathers commute times using Google Maps at 5 minute intervals using 'data_collection.py'.  A flask server (using 'ct_server.py') is used to display the data in a web page with the help of Bootstrap and Plotly(Javascript). Data can be displayed with a history of up to 10 days.  It can also be broken down per day of the week as well as all weekdays and weekends.  The original motivation was to visialize commute times between two destinations in a congested city to discern optimal travel times.

'tokens_and_addresses.py' must be filled out with MySQL server login details, Google Maps API key, location data, and location names list before data collection and webserver can function.

Installation requirements listed in 'requirements.txt'.

The result is currently on Amazon AWS EC2 and RDS instances.  It will occasionally be taken down for updates.  The link is below:
http://144.202.10.113/default/
