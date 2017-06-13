# coding: utf8

from flask import Flask, redirect, url_for, request, jsonify, abort
import sqlite3
import nmap
import time
import storage

app = Flask(__name__)

@app.route('/')
def index():
	return redirect(url_for('static', filename='index.html'))

@app.route('/getActiveNames')
def getActiveNames():
	activeUsers = storage.getActiveUsers(30*60)
	return jsonify(activeUsers)

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
	
	storage.saveUsername(name, ip2mac[ip])


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
