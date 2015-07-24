from django.conf.urls import patterns, include, url
from django.contrib import admin

import web_copo.views as views


#from allauth import *

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^copo/', include('web_copo.urls', namespace='copo')),
                       url(r'^rest/', include('web_copo.rest_urls', namespace='rest')),
                       url(r'^api/', include('web_copo.api_urls', namespace='api')),
                       (r'^accounts/', include('allauth.urls')),
                       (r'^accounts/profile/', views.index),
                       )
