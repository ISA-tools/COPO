#!/usr/bin/env python
import sys
import platform

import os

web_home = os.path.dirname(os.path.realpath(__file__ ))
proj_home = os.path.abspath(os.path.join(web_home, os.pardir))

if __name__ == "__main__":
    system = platform.system()
    #sys.path.append(web_home)
    sys.path.append(proj_home)
    sys.path.append(os.path.join(proj_home, 'api'))
    sys.path.append(os.path.join(proj_home, 'dal'))
    sys.path.append(os.path.join(web_home, 'project_copo'))
    sys.path.append(os.path.join(web_home, 'project_copo', 'settings'))
    sys.path.append(os.path.join(web_home, 'apps'))

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_copo.settings.master_settings")
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
