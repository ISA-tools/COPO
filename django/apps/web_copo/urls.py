from django.conf.urls import patterns, url

from apps.web_copo import views

urlpatterns = patterns('apps.web_copo.views',
                       url(r'^$', 'index', name='index'),
                       url(r'^testing/', views.view_test, name='test'),
                       url(r'^testing2/', views.view_test2, name='test'),
                       url(r'^login/', 'copo_login', name='login'),
                       url(r'^logout/', 'copo_logout', name='logout'),
                       url(r'^register/', 'copo_register', name='register'),
                       url(r'^new_profile/', views.new_profile, name='new_bundle'),
                       url(r'^profile/(?P<profile_id>[a-z0-9]+)/view', views.view_profile, name='view_profile'),
                       url(r'^new_collection/', views.new_collection_head, name='new_collection'),
                       url(r'^collection/(?P<collection_id>[a-z0-9]+)/view', views.view_collection, name='view_collection'),
                       url(r'^profile/(?P<profile_id>\d+)/view', views.view_profile, name='view_profile'),
                       url(r'^new_collection/', views.new_collection, name='new_collection'),
                       url(r'^collection/(?P<collection_id>\d+)/view', views.view_collection, name='view_collection'),
                       url(r'^repo_feedback/$', 'manage_repo_feedback', name='repo_feedback'),
                       url(r'^initiate_repo/$', 'initiate_repo', name='initiate_repo'),
)