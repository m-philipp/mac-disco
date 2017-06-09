# coding: utf8

# TODO:
# - do something with multiple names for one mac
# - parse the result in the view
# - ceantralize table creation and init as text/int fields
# - deduplicate the ip2mac code

from flask import Flask, redirect, url_for, request, jsonify, abort
import sqlite3
import nmap
import time

app = Flask(__name__)

@app.route('/')
def index():
	return redirect(url_for('static', filename='index.html'))

@app.route('/getActiveNames')
def getActiveNames():
	timestamp = time.time() - 30*60 # 30 Minutes ago
	query = '''
		SELECT 
			newestName2Mac.name,
			MAX(seenMacs.timestamp) as timestamp 
		FROM seenMacs 
		INNER JOIN 
			(
				select mac,
				(
					select name
					from name2macs as t2
					where t.mac = t2.mac
					order by rowid desc limit 1
				) as name
				from name2macs as t
				group by mac
			) as newestName2Mac 
		on seenMacs.mac = newestName2Mac.mac
		WHERE timestamp>'''+str(timestamp)+'''
		GROUP BY newestName2Mac.name
		'''
	# results in:
	# hans | 1496271433
	# peter | 1496201475
	
	conn = sqlite3.connect("macStore.db")
	c = conn.cursor()
	c.execute(query)
	rows = c.fetchall()
	conn.close()
	return jsonify(rows)

@app.route('/saveName')
def saveName():
	remoteIp = request.remote_addr;
	name = request.args.get('userName')
	if not remoteIp.startswith("192.168"):
		abort(400)
	store(name, remoteIp)
	return ''

def store(name, ip):
	ip2mac = getIp2Mac()
	if not ip in ip2mac:
		return
	
	conn = sqlite3.connect("macStore.db")
	c = conn.cursor()
	c.execute("CREATE TABLE IF NOT EXISTS name2macs (name, mac)")
	
	c.execute("INSERT INTO name2macs (name, mac) VALUES ('"+name+"','"+ip2mac[ip]+"')")
	conn.commit()
	conn.close()


def getIp2Mac():
	ip2mac = {}
	f = open('/proc/net/arp', 'r')
	for line in f:
		parts = line.split()
		if parts[0] == 'IP':
			continue
		ip2mac[parts[0]] = parts[3]
	f.close()
	return ip2mac

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8080, debug=True)
