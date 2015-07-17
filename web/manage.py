#!/usr/bin/env python
import sys

import os

if __name__ == "__main__":

    #pdb.set_trace()
    sys.path.append('/var/www/copo_www/COPO/web/apps')
    sys.path.append('/var/www/copo_www/COPO/web/project_copo')
    sys.path.append('/Users/fshaw/Dropbox/tgac_dev/prototypes/COPO/web/project_copo/settings/')
    sys.path.append('/Users/fshaw/Dropbox/tgac_dev/prototypes/COPO/web/apps/')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.settings")


    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

