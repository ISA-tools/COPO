#!/usr/bin/env python

import subprocess


# check and start mysql server if not running
proc = subprocess.Popen(["pgrep","mysql"], stdout=subprocess.PIPE)
out, err = proc.communicate()
if not err:
    if len(out.decode("utf-8")) > 0:
        print("MySQL is running.")
    else:
        print("Attempting to start MySQL server...")
        print(subprocess.call(["which","mysql"]))
        # proc1 = subprocess.Popen(["which", "mysql"], stdout=subprocess.PIPE)
        # proc1 = subprocess.Popen('which mysql', executable='/usr/bin/sh', shell=True)
        # out, err = proc1.communicate()
        # pth = proc1.stdout.read().decode("utf-8").strip()
        # subprocess.call([pth+".server", "start"])
else:
    print("MySQL - Cannot determine server's status.")

# check and start redis server if not running
# proc = subprocess.Popen(["pgrep","redis-server"], stdout=subprocess.PIPE)
# out, err = proc.communicate()
# if not err:
#     if len(out.decode("utf-8")) > 0:
#         print("Redis is running.")
#     else:
#         print("Attempting to start Redis server...")
#         proc1 = subprocess.Popen(["which", "redis-server"], stdout=subprocess.PIPE)
#         pth = proc1.stdout.read().decode("utf-8").strip()
#         subprocess.call([pth, "/usr/local/etc/redis.conf"])
# else:
#     print("Redis - Cannot determine server's status.")
#
# check and start mongo db if not running
proc = subprocess.Popen(["pgrep","mongod"], stdout=subprocess.PIPE)
out, err = proc.communicate()
if not err:
    if len(out.decode("utf-8")) > 0:
        print("Mongo is running.")
    else:
        print("Attempting to start MongoDB...")
        # cmd = "which mongod"
        # kk = subprocess.Popen(['/bin/bash', '-c', cmd])
        # proc1 = subprocess.Popen(["which", "mongod"], stdout=subprocess.PIPE)
        # out, err = kk.communicate()
        #pth = proc1.stdout.read().decode("utf-8").strip()
        #cmd = pth+" --fork --logpath ~/logs/mongo/mongodb.log"
        print(out)
        # subprocess.Popen(['/bin/bash', '-c', cmd])
        #subprocess.call([pth, " --fork --logpath ~/logs/mongo/mongodb.log"])
        #subprocess.call([pth])
        # status = subprocess.call(pth, shell=True)
        #status = subprocess.call(pth+" --fork --logpath ~/logs/mongo/mongodb.log", shell=True)
else:
    print("Mongo - Cannot determine server's status.")

