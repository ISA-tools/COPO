from django.conf.urls import patterns, url

import apps.web_copo.views as views
from apps.web_copo.mongo.figshare_da import *

urlpatterns = patterns('apps.web_copo.views',
                       url(r'^$', 'index', name='index'),
                       url(r'^login/', views.copo_login, name='login'),
                       url(r'^logout/', 'copo_logout', name='logout'),
                       url(r'^register/', 'copo_register', name='register'),
                       url(r'^new_profile/', 'new_profile', name='new_bundle'),
                       url(r'^profile/(?P<profile_id>[a-z0-9]+)/view', 'view_profile', name='view_profile'),
                       url(r'^new_collection/', 'new_collection_head', name='new_collection'),
                       url(r'^collection/(?P<collection_head_id>[a-z0-9]+)/view', 'view_collection', name='view_collection'),
                       url(r'^profile/(?P<profile_id>\d+)/view', 'view_profile', name='view_profile'),
                       url(r'^new_collection/', 'new_collection_head', name='new_collection'),
                       url(r'^collection/(?P<collection_head_id>\d+)/view', 'view_collection', name='view_collection'),
                       url(r'^initiate_repo/$', 'initiate_repo', name='initiate_repo'),
                       url(r'^add_to_collection/$', 'add_to_collection', name='add_to_collection'),
                       url(r'^add_to_study/$', 'add_to_study', name='add_to_study'),
                       url(r'^remove_from_collection/$', 'remove_from_collection', name='remove_from_collection'),
                       url(r'^study/(?P<study_id>.*)/view', 'view_study', name='view_study'),
                       url(r'^study/(?P<study_id>\d+)/view', 'view_study', name='view_study'),

                       url(r'^save_article/$', FigshareCollection().save_article, name='save_article'),


                       url(r'^register_to_irods/$', 'register_to_irods', name='register_to_irods'),
                       url(r'^ena_template/$', 'ena_template', name='ena_template'),


)

