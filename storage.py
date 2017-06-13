# coding: utf8
import sqlite3
import time

sqliteDB = "macStore.db"
createSeenMacsTable = "CREATE TABLE IF NOT EXISTS seenMacs (timestamp INTEGER, mac TEXT)"
createName2macsTable = "CREATE TABLE IF NOT EXISTS name2macs (name TEXT, mac TEXT)"

# store the online mac adresses in the sqlite table
def saveOnlineMacAdresses(adresses):
	conn = sqlite3.connect(sqliteDB)
	c = conn.cursor()
	c.execute(createSeenMacsTable)

	for mac in adresses:
		c.execute("INSERT INTO seenMacs (timestamp, mac) VALUES ("+str(time.time())+",'"+mac+"')")

	conn.commit()
	conn.close()


def saveUsername(name, mac):
	conn = sqlite3.connect(sqliteDB)
	c = conn.cursor()
	c.execute(createName2macsTable)
	
	c.execute("INSERT INTO name2macs (name, mac) VALUES ('"+name+"','"+mac+"')")
	conn.commit()
	conn.close()


def getActiveUsers(secondsAgo):
	timestamp = time.time() - secondsAgo 
	# this gets the users online after the timestamp
	# with username and the last seen time
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
	
	conn = sqlite3.connect(sqliteDB)
	c = conn.cursor()
	c.execute(query)
	rows = c.fetchall()
	conn.close()
	print(rows)
	return rows
