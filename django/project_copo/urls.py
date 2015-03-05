from django.conf.urls import patterns, include, url

from django.contrib import admin
from rest_framework import routers

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'project_copo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^copo/', include('apps.web_copo.urls', namespace='copo')),
    url(r'^rest/', include('apps.web_copo.rest_urls', namespace='rest')),
)
