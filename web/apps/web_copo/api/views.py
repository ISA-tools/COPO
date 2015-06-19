__author__ = 'felix.shaw@tgac.ac.uk - 14/05/15'

import pycurl
from urllib.parse import urlencode

import requests
import jsonpickle
from io import BytesIO

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


def handle_orcid_authorise(code):
    c = pycurl.Curl()
    buffer = BytesIO()

    url = REPOSITORIES['ORCID']['urls']['ouath/token'] + 'client_id=' + REPOSITORIES['ORCID']['client_id'] + '&client_secret=' + REPOSITORIES['ORCID']['client_secret'] + '&' \
          'grant_type=authorization_code&code=' + code + '&redirect_uri=' + REPOSITORIES['ORCID']['urls']['redirect']


    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, buffer)

    #c.setopt(c.POST, 1)
    postdata = {'key':'value'}
    postdata = urlencode(postdata)
    c.setopt(c.POSTFIELDS, postdata)
    c.perform()


    body = buffer.getvalue()
    response = jsonpickle.decode(body)

    access_token = response['access_token']
    orcid_id = response['orcid']

    '''
    access_token = 'cd8288f1-4e53-44b3-95ef-abcf9a4742be'
    orcid_id = '0000-0001-7572-1265'
    '''

    c = pycurl.Curl()
    url = 'http://pub.sandbox.orcid.org/v1.2/' + orcid_id + '/orcid-profile/'
    print(url)
    c.setopt(c.URL, url)
    c.setopt(c.HTTPHEADER, ['Accept: application/orcid+json'])
    buffer = BytesIO()
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()

    out = buffer.getvalue()
    print(out.decode('iso-8859-1'))