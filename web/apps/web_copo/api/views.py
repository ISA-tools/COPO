__author__ = 'felix.shaw@tgac.ac.uk - 14/05/15'

import requests
from django.http import HttpResponse
import jsonpickle

import web_copo.repos.figshare as f
import dal.figshare_da as fs
from dal.figshare_da import FigshareCollection
from services import *
from dal.copo_base_da import DataSchemas
from web_copo.uiconfigs.utils.data_formats import DataFormats


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

    # purify output (...again!) and store a copy in DB
    if temp_dict["status"] == "success" and temp_dict["data"]:
        temp_dict["data"] = DataFormats("ENA").purify(temp_dict["data"])
        DataSchemas("ENA").add_ui_template(temp_dict["data"])

    return HttpResponse(jsonpickle.encode(temp_dict))

