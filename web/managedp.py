#!/usr/bin/env python3
__author__ = 'tonietuk'

import sys
import subprocess

subprocess.check_output(str(sys.argv[1]), shell=True)
