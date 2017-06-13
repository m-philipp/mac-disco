# mac-disco

disco disco ...


## flaskServer

	./startup.sh

This needs gunicorn installed.

## macScanner

The macScanner needs to run as root. This is necessary since ICMP request don't succesfully retrieve all devices in a network (e.g. Windows 10 doesn't respone to ICMP request).

The macScanner needs to run periodically. To do that you might want to use cronjobs or somethins similar.


## Needed Python packages

* flask
* nmap
* sqlite3
