import sqlite3
import nmap
import time


# use nmap to scan for ICMP host scan
nm = nmap.PortScanner()
nm.scan(hosts='192.168.0.0/24', arguments='-sn')
hosts = nm.all_hosts()

# sleep a while to make sure the ARP discovery from the nmap call is finished
# prop not necessary
time.sleep(3)

# get the mac adresses from arp storage
ip2mac = {}
f = open('/proc/net/arp', 'r')
for line in f:
	parts = line.split()
	if parts[0] == 'IP':
		continue
	ip2mac[parts[0]] = parts[3]
f.close()

# store the MAC adresses of the hosts online
onlineMacs = []
for host in hosts:
	if host in ip2mac:
		onlineMacs.append(ip2mac[host])
print onlineMacs

# store the online mac adresses in the sqlite table
conn = sqlite3.connect("macStore.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS macs (timestamp, mac)")

for mac in onlineMacs:
	c.execute("INSERT INTO macs VALUES ("+str(time.time())+",'"+mac+"')")

conn.commit()
conn.close()