__author__ = 'felix.shaw@tgac.ac.uk - 29/04/15'

import json

from django.http import HttpResponse
import jsonpickle

from apps.web_copo.oauth_utils.copo_oauth1 import *


client = requests.session()
json_header = {'content-type': 'application/json'}


def check_figshare_credentials(request):
    # this method called from JS frontend - if credentials exist, set a session variable containing
    # the oauth object and return true. If credentials don't exist, send redirect URL to frontend and return false
    if (Figshare_token().token_exists()):

        #else retrieve saved tokens and validate
        tokens = Figshare_token().get_token_from_db()
        if(not valid_tokens(tokens)):
            Figshare_token().delete_old_token()
            tokens = get_authorize_url()

        resource_owner_key = tokens['owner_key']
        resource_owner_secret = tokens['owner_secret']
        request.session['figshare_credentials'] = OAuth1(client_key,
                      client_secret=client_secret,
                      resource_owner_key=resource_owner_key,
                      resource_owner_secret=resource_owner_secret,
                      signature_type='auth_header')
        out = {}
        out['exists': True]
    else:
        #if no token exists in the database
        out = {}
        out['exists'] = False
        out['url'] = get_authorize_url()

    return HttpResponse(jsonpickle.encode(out))


def make_article(oauth=None):
    url = 'http://api.figshare.com/v1/my_data/articles'
    body = {'title': 'COPO ARTICLE', 'description': 'COPO DESCRIPTION', 'defined_type': 'paper'}
    response = client.post(url, auth=oauth, data=json.dumps(body), headers=json_header)
    return json.loads(response.content.decode("utf-8"))


def delete_article(oauth=None, article_id=0):
    response = client.delete('http://api.figshare.com/v1/my_data/articles/' + str(article_id), auth=oauth)
    return json.loads(response.content.decode("utf-8"))

def get_my_articles(oauth=None):
    url = 'http://api.figshare.com/v1/my_data/articles'
    response = client.get(url, auth=oauth, headers=json_header)
    return json.loads(response.content.decode("utf-8"))


def add_file_to_article(oauth=None, article_id=0, filename=''):
    url = 'http://api.figshare.com/v1/my_data/articles/' + str(article_id) + '/files'
    files = {'filedata': (filename, open(filename, 'rb'))}
    response = client.put(url, auth=oauth, files=files)
    return json.loads(response.content.decode("utf-8"))


def add_tags_to_article(oauth=None, article_id=0, tag=''):
    tag = {'tag_name': tag}
    response = client.put('http://api.figshare.com/v1/my_data/articles/' + str(article_id) + '/tags', auth=oauth,
                          data=json.dumps(tag), headers=json_header)
    return json.loads(response.content.decode("utf-8"))