from django.conf.urls import patterns, url
#import apps.web_copo.rest.EnaRest as rest
from apps.chunked_upload.views import *

urlpatterns = patterns('apps.web_copo.rest.EnaRest',
                       url(r'^ena_sample_form/', 'get_ena_sample_controls', name='get_ena_sample_controls'),
                       url(r'^ena_new_study/', 'save_ena_study', name='save_ena_study'),
                       url(r'^ena_new_sample/', 'save_ena_sample_callback', name='save_ena_sample'),
                       url(r'^populate_samples_form/', 'populate_samples_form', name='populate_samples_form'),
                       url(r'^get_sample_html/(?P<sample_id>\d+)', 'get_sample_html', name='get_sample_html'),
                       url(r'^get_sample_html/', 'get_sample_html', name='get_sample_html_param'),
                       url(r'^populate_data_dropdowns/', 'populate_data_dropdowns', name='populate_data_dropdowns'),
                       url(r'^get_instrument_models/', 'get_instrument_models', name='get_instrument_models'),
                       url(r'^get_experimental_samples/', 'get_experimental_samples',
                           name='get_experimental_samples'),
                       url(r'^receive_data_file/', 'receive_data_file', name='receive_data_file'),
                       url(r'^receive_data_file_chunked/', ChunkedUploadView.as_view(), name='receive_data_file'),
                       url(r'^complete_upload/', ChunkedUploadCompleteView.as_view(), name='complete_data_file'),
                       url(r'^hash_upload/', 'hash_upload', name='hash_upload'),
                       url(r'^inspect_file/', 'inspect_file', name='inspect_file'),
                       url(r'^zip_file/', 'zip_file', name='zip_file'),
                       url(r'^save_experiment/', 'save_experiment', name='save_experiment'),
                       url(r'^get_experiment_table_data/', 'get_experiment_table_data', name='get_experiment_table_data'),
                       url(r'^get_experiment_modal_data/', 'populate_exp_modal', name='populate_exp_modal'),
                       url(r'^delete_file/', 'delete_file', name='delete_file'),

)