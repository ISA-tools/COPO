#!/usr/bin/env python
import sys
import platform

import os

home = os.path.dirname(os.path.realpath(__file__ ))
print(home)


if __name__ == "__main__":
    system = platform.system()
    sys.path.append(home)
    sys.path.append(os.path.join(home, 'project_copo'))
    sys.path.append(os.path.join(home, 'apps'))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_copo.settings.settings")
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
