#!/usr/bin/env python3

import os
from os.path import expanduser
import subprocess
import shutil


def check_status(process_name, display_name):
    process = subprocess.Popen(["pgrep", process_name], stdout=subprocess.PIPE)
    out, err = process.communicate()
    if not err:
        if len(out.decode("utf-8")) > 0:
            print(display_name + " is running.")
            return 0  # service running
        else:
            return 1  # service not running
    else:
        return -1  # can't determine service status


def start_service(process_name, display_name, start_args):
    status = check_status(process_name, display_name)
    if status == 1:
        print("Attempting to start " + display_name + "...")
        output = subprocess.check_output(start_args, shell=True)
        check_status(process_name, display_name)
    elif status == -1:
        print(display_name + " - can't determine service status!")


start_service("mysql", "MySQL server", shutil.which("mysql")+".server start")
start_service("redis-server", "Redis server", shutil.which("redis-server")+" /usr/local/bin/redis.conf")

log_path = "~/logs/mongo/mongolog.log"
start_service("mongod", "MongoDB", shutil.which("mongod")+" --fork --logpath %s" % log_path)
