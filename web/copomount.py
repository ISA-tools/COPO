#!/usr/bin/env python3
__author__ = 'tonietuk'

import os
import re
import sys
import time
import pexpect
import subprocess

user_token = "etuka"
host_token = "v0546.nbi.ac.uk"
remote_path_token = "/usr/users/ga002/etuka/copo-data/"
mount_name = "COPOIrodsMount"
home_directory = os.path.expanduser("~")  # this could point to any path
mount_point = os.path.join(home_directory, mount_name)
remote_connect = user_token+"@"+host_token+":"+remote_path_token
vol_name = "COPO_v0546"  # this could be named anything
password = "RwvmPMC7"  # TODO: get me outta here!

cmd = ""
cmd += "sshfs -p 22 {remote_connect!s} {mount_point!s} -oauto_cache,reconnect,".format(**locals())
cmd += "defer_permissions,noappledouble,negative_vncache,volname={vol_name!s}".format(**locals())

ping_messages = [
    "0 packets received",
    "destination host unreachable",
    "request timed out",
    "unknown host"
]

# check if remote host is available
process = subprocess.Popen(["ping", "-c", "1", host_token], stdout=subprocess.PIPE).communicate()
if process[0]:
    for p_m in ping_messages:
        if p_m.lower() in process[0].decode("utf-8").lower():
            sys.exit("Host may be unreachable, exiting...")


# check if mount exists
process = subprocess.Popen(["df"], stdout=subprocess.PIPE)  # 'df' lists all mount points, could also use 'mount'
out, err = process.communicate()
if mount_name in out.decode("utf-8"):
    print("'"+remote_connect + "' already mounted on '%s'" % mount_point)
else:
    # create mount point
    if not os.path.exists(mount_point):
        print("Creating mount point '%s'..." % mount_point)
        status = subprocess.call(["mkdir", "-p", mount_point])
        if status == 0:
            print("Mount point successfully created, mounting remote directory...")
        else:
            sys.exit("Cannot create mount point, exiting...")
    else:
        print("Mounting '" + remote_connect + "' on '" + mount_point + "'...")
        time.sleep(2)

    # mount the remote directory
    thread = pexpect.spawn(cmd, timeout=None)
    thread.expect(["assword:", pexpect.EOF])
    thread.sendline(password)
    thread.expect(pexpect.EOF)
    s = thread.before.decode("utf-8")
    regex = re.compile(r'[\n\r\t]')
    s = regex.sub('', s)
    if len(s.strip(' ')) == 0:
        print("Successfully mounted '%s'!" % mount_point)
    else:
        print("Couldn't mount remote directory, exiting...")