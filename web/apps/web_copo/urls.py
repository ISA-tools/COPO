from django.conf.urls import patterns, url
import apps.web_copo.views as views
urlpatterns = patterns('apps.web_copo.views',
                       url(r'^$', 'index', name='index'),
                       url(r'^login/', views.copo_login, name='login'),
                       url(r'^logout/', 'copo_logout', name='logout'),
                       url(r'^register/', 'copo_register', name='register'),
                       url(r'^new_profile/', 'new_profile', name='new_bundle'),
                       url(r'^profile/(?P<profile_id>[a-z0-9]+)/view', 'view_profile', name='view_profile'),
                       url(r'^new_collection/', 'new_collection_head', name='new_collection'),
                       url(r'^collection/(?P<collection_id>[a-z0-9]+)/view', 'view_collection', name='view_collection'),
                       url(r'^profile/(?P<profile_id>\d+)/view', 'view_profile', name='view_profile'),
                       url(r'^new_collection/', 'new_collection_head', name='new_collection'),
                       url(r'^collection/(?P<collection_id>\d+)/view', 'view_collection', name='view_collection'),
                       url(r'^repo_feedback/$', 'manage_repo_feedback', name='repo_feedback'),
                       url(r'^initiate_repo/$', 'initiate_repo', name='initiate_repo'),
)