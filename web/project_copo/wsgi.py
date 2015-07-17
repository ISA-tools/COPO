"""
WSGI config for project_copo project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import sys

import os




#sys.path.append('/var/www/copo_www/COPO/web/project_copo/settings/')
sys.path.append('/var/www/copo_www/COPO/web')
sys.path.append('/var/www/copo_www/COPO/web/apps')
#sys.path.append('/var/www/copo_www/COPO/web/apps/allauth')


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

#import django.core.handlers.wsgi
#application = django.core.handlers.wsgi.WSGIHandler()
