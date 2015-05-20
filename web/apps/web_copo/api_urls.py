__author__ = 'felix.shaw@tgac.ac.uk - 14/05/15'

from django.conf.urls import patterns, url

import apps.web_copo.api.views as api_views


urlpatterns = patterns('',
    url(r'^submit_to_figshare/(?P<article_id>[a-z0-9]+)', api_views.submit_to_figshare, name='submit_figshare_collection'),
)