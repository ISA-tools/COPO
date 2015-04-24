#! /usr/bin/python

import subprocess

# check and start mysql server if not running
proc = subprocess.Popen(["mysqladmin", "-umysql", "ping"], stdout=subprocess.PIPE)
out, err = proc.communicate()
if not err:
	if "alive" in out.decode("utf-8").lower():
		print("MySQL is running.")
	else:
		print("Attempting to start MySQL server...")
		subprocess.call(["mysql.server", "start"])


# check and start redis server if not running
proc = subprocess.Popen(["redis-cli", "ping"], stdout=subprocess.PIPE)
out, err = proc.communicate()
if not err:
	if "pong" in out.decode("utf-8").lower():
		print("Redis is running.")
	else:
		print("Attempting to start Redis server...")
		subprocess.call(["redis-server", "/usr/local/etc/redis.conf"])
