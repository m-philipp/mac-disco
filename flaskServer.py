# coding: utf8

from flask import Flask, redirect, url_for, request, jsonify, abort
import sqlite3
import nmap


app = Flask(__name__)

@app.route('/')
def index():
	return redirect(url_for('static', filename='index.html'))

@app.route('/saveName')
def saveName():
	remoteIp = request.remote_addr;
	name = request.args.get('userName')
	if not remoteIp.startswith("192.168"):
		abort(400)
	store(name, remoteIp)


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
