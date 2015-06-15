__author__ = 'felix.shaw@tgac.ac.uk - 14/05/15'

from django.conf.urls import patterns, url

import apps.web_copo.api.views as api_views

import apps.web_copo.uiconfigs.utils.data_formats as dfmts

urlpatterns = patterns('',
    url(r'^submit_to_figshare/(?P<article_id>[a-z0-9]+)', api_views.submit_to_figshare, name='submit_figshare_collection'),
    url(r'^get_figshare_url/(?P<article_id>[a-z0-9]+)', api_views.view_in_figshare, name='view_figshare_collection'),
    url(r'^delete_figshare_article/(?P<article_id>[a-z0-9]+)', api_views.delete_from_figshare, name='delete_article'),
    url(r'^refactor_ui_template_ena/$', dfmts.refactor_ui_template_ena, name='refactor_ui_template_ena'),
                       )

