from django.conf.urls import url
from . import views
from web.apps.web_copo.utils import ajax_handlers

urlpatterns = [url(r'^$', views.index, name='index'),
               url(r'^test_submission', views.test_submission, name='test_submission'),
               url(r'^test_pdf', views.test_pdf, name='test_pdf'),
               url(r'^test', views.test, name='test'),
               url(r'^login', views.login, name='auth'),
               url(r'^logout/', views.copo_logout, name='logout'),
               url(r'^register/', views.copo_register, name='register'),
               url(r'^profile/update_counts/', views.get_profile_counts, name='update_counts'),
               url(r'^view_orcid_profile/$', views.view_orcid_profile, name='view_orcid_profile'),
               url(r'^error/', views.goto_error, name='error_page'),
               url(r'^register_to_irods/$', views.register_to_irods, name='register_to_irods'),
               # urls from October 2015 refactor below
               url(r'^copo_profile/(?P<profile_id>[a-z0-9]+)/view', views.view_copo_profile,
                   name='view_copo_profile'),
               url(r'^copo_publications/(?P<profile_id>[a-z0-9]+)/view', views.copo_publications,
                   name='copo_publications'),
               url(r'^copo_data/(?P<profile_id>[a-z0-9]+)/view', views.copo_data,
                   name='copo_data'),
               url(r'^copo_samples/(?P<profile_id>[a-z0-9]+)/view', views.copo_samples,
                   name='copo_samples'),
               url(r'^copo_submissions/(?P<profile_id>[a-z0-9]+)/view', views.copo_submissions,
                   name='copo_submissions'),
               url(r'^copo_people/(?P<profile_id>[a-z0-9]+)/view', views.copo_people,
                   name='copo_people'),
               url(r'^copo_annotation/(?P<profile_id>[a-z0-9]+)/view', views.copo_annotation,
                   name='copo_annotation'),
               url(r'^get_source_count/$', ajax_handlers.get_source_count,
                   name="get_source_count"),
               url(r'^ajax_search_ontology/(?P<ontology_names>[a-z0-9]+(,[a-z0-9]+)*)/$',
                   ajax_handlers.search_ontology_ebi, name='ajax_search_ontology'),
               url(r'^ajax_search_ontology_test/$', ajax_handlers.test_ontology, name='test_ontology'),
               url(r'^copo_forms/$', views.copo_forms, name="copo_forms"),
               url(r'^copo_visualize/$', views.copo_visualize, name="copo_visualize"),
               url(r'^authenticate_figshare/$', views.authenticate_figshare, name='authenticate_figshare'),
               url(r'^publish_figshare/$', ajax_handlers.publish_figshare, name='publish_figshare'),
               url(r'^view_oauth_tokens/$', views.view_oauth_tokens, name='view_oauth_tokens'),
               url(r'^get_tokens_for_user/$', ajax_handlers.get_tokens_for_user, name='get_tokens_for_user'),
               url(r'^delete_token/$', ajax_handlers.delete_token, name='delete_token'),
               url(r'^get_annotation/$', views.annotate_data, name='annotate_data'),

               ]
