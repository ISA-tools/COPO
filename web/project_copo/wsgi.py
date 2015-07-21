"""
WSGI config for project_copo project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import sys

import os

home = os.path.dirname(os.path.realpath(__file__ ))

sys.path.append(home)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'apps')))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", ".settings.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

#import django.core.handlers.wsgi
#application = django.core.handlers.wsgi.WSGIHandler()
