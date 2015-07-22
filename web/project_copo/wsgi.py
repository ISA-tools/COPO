"""
WSGI config for project_copo project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import sys

import os


#home = os.path.dirname(os.path.realpath(__file__ ))
home = '/var/www/copo_www/COPO/web/project_copo'
logfile_name = os.path.join(home, 'logs', 'wsgi_log.txt')
#sys.stdout = open(logfile_name, 'w+')



#sys.path.append(home)
#p = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'apps'))
#print(p)
#sys.path.append(p)

sys.path.append('/var/www/copo_www/COPO/web/project_copo')
sys.path.append('/var/www/copo_www/COPO/web/apps')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

#import django.core.handlers.wsgi
#application = django.core.handlers.wsgi.WSGIHandler()
