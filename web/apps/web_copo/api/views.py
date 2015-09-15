__author__ = 'felix.shaw@tgac.ac.uk - 14/05/15'

import requests
from django.http import HttpResponse
import jsonpickle
import json

import web.apps.web_copo.repos.figshare as f
import dal.figshare_da as fs
from dal.figshare_da import FigshareCollection
from services import *
from dal.copo_base_da import DataSchemas
from web.apps.web_copo.copo_maps.utils.data_formats import DataFormats
from api.doi_metadata import DOI2Metadata


def upload_to_figshare_profile(request):
    if request.method == 'POST':
        user = request.user
        file = request.FILES['file']
        repo_type = request.POST['repo']
        out = fs.FigshareCollection.receive_data_file(file, repo_type, user)
        return HttpResponse(out, content_type='json')


def submit_to_figshare(request, article_id):
    # check status of figshare collection
    if FigshareCollection().is_clean(article_id):
        # there are no changes to the collection so don't submit
        data = {'success': False}
        return HttpResponse(jsonpickle.encode(data))
    else:
        # get collection_details
        details = FigshareCollection().get_collection_details_from_collection_head(article_id)
        for d in details['collection_details']:
            figshare_article_id = f.submit_to_figshare(d)
            if (figshare_article_id != None):
                # figshare_article_id is the Figshare article id
                FigshareCollection().mark_as_clean(article_id)
                data = {'success': True}
        return HttpResponse(jsonpickle.encode(data))


def view_in_figshare(request, article_id):
    url = FigshareCollection().get_url(article_id)
    return HttpResponse(jsonpickle.encode(url))


def delete_from_figshare(request, article_id):
    if (f.delete_from_figshare(article_id)):
        collection_id = request.session["collection_head_id"]
        FigshareCollection().delete_article(article_id, collection_id)

        data = {'success': True}
    else:
        data = {'success': False}
    return HttpResponse(jsonpickle.encode(data))


def login_orcid(request):
    r = requests.get(
        'https://sandbox.orcid.org/oauth/authorize?client_id=0000-0002-4011-2520&response_type=code&scope=/authenticate&redirect_uri=http://www.127.0.0.1/copo')
    return HttpResponse('ere we go')


def check_orcid_credentials(request):
    # TODO - here we check if the orcid tokens are valid
    out = {'exists': False, 'authorise_url': REPOSITORIES['ORCID']['urls']['authorise_url']}
    return HttpResponse(jsonpickle.encode(out))


# call only if you want to generate a new template
def generate_ena_template(request):
    temp_dict = DataFormats("ENA").generate_ui_template()
    return HttpResponse(jsonpickle.encode(temp_dict))


def doi2publication_metadata(request, id_handle):
    if id_handle:
        out_dict = DOI2Metadata(id_handle).publication_metadata()
    else:
        message = "DOI missing"
        out_dict = {"status": "failed", "messages": message, "data": {}}
    return HttpResponse(jsonpickle.encode(temp_dict))

def get_collection_type(request):
    from dal.copo_base_da import Collection_Head
    collection_id = request.GET['collection_id']
    c = Collection_Head().GET(collection_id)
    return HttpResponse(c['type'])

def convert_to_sra(request):
    from converters.ena.copo_hokey import exporter
    from services import EXPORT_LOCATIONS
    collection_id = request.POST['collection_id']
    if exporter().do_validate(collection_id):
        exporter().do_export(collection_id, EXPORT_LOCATIONS['ENA']['export_path'])
    return HttpResponse('here')

    return HttpResponse(json.dumps(out_dict, ensure_ascii=False))
