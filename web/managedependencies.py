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
else:
    print("MySQL - Cannot determine server's status.")

# check and start redis server if not running
proc = subprocess.Popen(["redis-cli", "ping"], stdout=subprocess.PIPE)
out, err = proc.communicate()
if not err:
    if "pong" in out.decode("utf-8").lower():
        print("Redis is running.")
    else:
        print("Attempting to start Redis server...")
        subprocess.call(["redis-server", "/usr/local/etc/redis.conf"])
else:
    print("Redis - Cannot determine server's status.")

# check and start mongo db if not running
proc = subprocess.Popen(["pgrep","mongod"], stdout=subprocess.PIPE)
out, err = proc.communicate()
if not err:
    if len(out.decode("utf-8")) > 0:
        print("Mongo is running.")
    else:
        print("Attempting to start MongoDB...")
        status = subprocess.call("mongod --fork --logpath ~/logs/mongo/mongodb.log", shell=True)
else:
    print("Mongo - Cannot determine server's status.")

