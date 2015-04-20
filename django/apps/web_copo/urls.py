from django.conf.urls import patterns, url

from apps.web_copo import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^testing/', views.view_test, name='test'),
                       url(r'^testing2/', views.view_test2, name='test2'),
                       url(r'^login/', views.copo_login, name='login'),
                       url(r'^logout/', views.copo_logout, name='logout'),
                       url(r'^register/', views.copo_register, name='register'),
                       url(r'^new_profile/', views.new_profile, name='new_bundle'),
                       url(r'^profile/(?P<profile_id>[a-z0-9]+)/view', views.view_profile, name='view_profile'),
                       url(r'^new_collection/', views.new_collection_head, name='new_collection'),
                       url(r'^collection/(?P<collection_id>[a-z0-9]+)/view', views.view_collection, name='view_collection'),
)