Install eveyrthing floowing Readme.md first

Install MySQL server:  https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-16-04

enter mysql cmd line with:  'mysql -u root -p'
create the commute2 database by running: CREATE DATABASE commute2;
exit mysql command line
run 'service mysql restart'

To bind the correct port, set 'bind-address' to '0.0.0.0' in /etc/mysql/mysql.conf.d/mysqld.cnf (http://devdocs.magento.com/guides/v2.0/install-gde/prereq/mysql_remote.html)

Run data collection silently with 'nohup python data_collection.py &'
Run webserver silently with 'gunicorn --workers=4 --bind=0.0.0.0:80 ct_server:app &'
