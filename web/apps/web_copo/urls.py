from django.conf.urls import patterns, url

import web.apps.web_copo.views as views

urlpatterns = patterns('web_copo.views',
                       url(r'^$', 'index', name='index'),

                       url(r'^logout/', 'copo_logout', name='logout'),
                       url(r'^register/', 'copo_register', name='register'),
                       url(r'^new_profile/', 'new_profile', name='new_bundle'),
                       url(r'^profile/(?P<profile_id>[a-z0-9]+)/view', 'view_profile', name='view_profile'),
                       url(r'^copo_profile/(?P<profile_id>[a-z0-9]+)/view', views.view_copo_profile, name='view_copo_profile'),
                       url(r'^new_collection/', 'new_collection_head', name='new_collection'),
                       url(r'^collection/(?P<collection_head_id>[a-z0-9]+)/view', 'view_collection',
                           name='view_collection'),
                       url(r'^profile/(?P<profile_id>\d+)/view', 'view_profile', name='view_profile'),
                       url(r'^new_collection/', 'new_collection_head', name='new_collection'),
                       url(r'^collection/(?P<collection_head_id>\d+)/view', 'view_collection', name='view_collection'),
                       url(r'^upload_to_dropbox/$', 'upload_to_dropbox', name='upload_to_dropbox'),
                       url(r'^view_orcid_profile/$', 'view_orcid_profile', name='view_orcid_profile'),
                       url(r'^add_to_collection/$', 'add_to_collection', name='add_to_collection'),
                       url(r'^add_to_study/$', 'add_to_study', name='add_to_study'),
                       url(r'^study/(?P<study_id>.*)/view', 'view_study', name='view_study'),
                       url(r'^study/(?P<study_id>\d+)/view', 'view_study', name='view_study'),
                       url(r'^error/', views.goto_error, name='error_page'),
                       url(r'^save_article/$', views.save_figshare_collection, name='save_article'),
                       url(r'^register_to_irods/$', 'register_to_irods', name='register_to_irods'),
                       )
