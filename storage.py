# coding: utf8
import sqlite3
import time

sqliteDB = "macStore.db"
createSeenMacsTable = "CREATE TABLE IF NOT EXISTS seenMacs (timestamp INTEGER, mac TEXT)"
createName2macsTable = "CREATE TABLE IF NOT EXISTS name2macs (name TEXT, mac TEXT)"

# store the online mac adresses in the sqlite table
def saveOnlineMacAdresses(adresses):
	print("saveOnlineMacAdresses")
	conn = sqlite3.connect(sqliteDB)
	print(".")
	c = conn.cursor()
	print(".")
	c.execute(createSeenMacsTable)
	print(".")

	for mac in adresses:
		c.execute("INSERT INTO seenMacs (timestamp, mac) VALUES ("+str(time.time())+",'"+mac+"')")

	print(".")
	conn.commit()
	print(".")
	conn.close()
	print("!")


def saveUsername(name, mac):
	print("saveUsernam")
	conn = sqlite3.connect(sqliteDB)
	print(".")
	c = conn.cursor()
	print(".")
	c.execute(createName2macsTable)
	print(".")
	
	c.execute("INSERT INTO name2macs (name, mac) VALUES ('"+name+"','"+mac+"')")
	print(".")
	conn.commit()
	print(".")
	conn.close()
	print("!")


def getActiveUsers(secondsAgo):
	print("getActiveUsers")
	timestamp = time.time() - secondsAgo 
	print(".")
	# this gets the users online after the timestamp
	print(".")
	# with username and the last seen time
	print(".")
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
	# hans | 1496271433		# laptop mac
	# hans | 1496271437		# mobile mac
	# peter | 1496201475
	print(".")
	
	conn = sqlite3.connect(sqliteDB)
	print(".")
	c = conn.cursor()
	print(".")
	c.execute(query)
	print(".")
	rows = c.fetchall()
	print(".")
	conn.close()
	print(".")
	print(rows)
	print("!")
	return rows
