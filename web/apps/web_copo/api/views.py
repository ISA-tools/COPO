__author__ = 'felix.shaw@tgac.ac.uk - 14/05/15'

import requests

from apps.web_copo.mongo.figshare_da import *
import apps.web_copo.repos.figshare as f
from project_copo.settings.services import *


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
        FigshareCollection().delete_article(request)

        data = {'success': True}
    else:
        data = {'success': False}
    return HttpResponse(jsonpickle.encode(data))


def login_orcid(request):
    r = requests.get(
        'https://sandbox.orcid.org/oauth/authorize?client_id=0000-0002-4011-2520&response_type=code&scope=/authenticate&redirect_uri=http://www.127.0.0.1/copo')
    print(r.status_code)
    print(r.json())
    return HttpResponse('ere we go')


def check_orcid_credentials(request):
    # TODO - here we check if the orcid tokens are valid
    out = {'exists': False, 'authorise_url': REPOSITORIES['ORCID']['urls']['authorise_url']}
    return HttpResponse(jsonpickle.encode(out))

