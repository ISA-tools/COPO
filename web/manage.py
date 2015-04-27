#!/usr/bin/env python
import os
import sys
import subprocess

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_copo.settings.settings")

    script_pth = os.path.join(os.path.dirname(os.path.abspath(__file__)), "managedependencies.py")

    print("path to script:", script_pth)

    pro_var = subprocess.Popen([sys.executable, script_pth])
    pro_var.communicate()

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)