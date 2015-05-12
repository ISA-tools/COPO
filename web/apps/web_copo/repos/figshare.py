__author__ = 'felix.shaw@tgac.ac.uk - 29/04/15'

import json
from urllib.parse import parse_qs

import requests
from django.http import HttpResponse
import jsonpickle
from requests_oauthlib import OAuth1, OAuth1Session
from django_tools.middlewares import ThreadLocal
from django.core.urlresolvers import reverse

from apps.web_copo.mongo.mongo_oauth_tokens import Figshare_token


client = requests.session()
json_header = {'content-type': 'application/json'}
client_key = 'id6JBVVeItadGDmjRUDljg'
client_secret = 'BC2tEMeCAT3veHhzfd2xIA'
resource_owner_key = ''
resource_owner_secret = ''
tokens = None



# figshare API methods
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

# Figshare OAUTH methods
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


def set_figshare_credentials(request):
    # call backend method to get and save access token to mongo
    get_access_token(request)
    return HttpResponse('<script>window.top.close();</script>')


def get_authorize_url():

    request_token_url = 'http://api.figshare.com/v1/pbl/oauth/request_token'
    authorization_url = 'http://api.figshare.com/v1/pbl/oauth/authorize'

    #Obtain request token
    request = ThreadLocal.get_current_request()
    domain = request.META['HTTP_HOST']
    callback_uri = 'http://' + domain + reverse('rest:set_figshare_credentials')
    oauth = OAuth1Session(client_key, client_secret=client_secret, callback_uri=callback_uri)
    fetch_response = oauth.fetch_request_token(request_token_url)
    request.session['resource_owner_key'] = fetch_response.get('oauth_token')
    request.session['resource_owner_secret'] = fetch_response.get('oauth_token_secret')

    #Obtain Authorize Token
    authorize_url = authorization_url + '?oauth_token='
    authorize_url = authorize_url + request.session['resource_owner_key']

    #redirect user to login page
    return authorize_url


def get_access_token(request):

    access_token_url = 'http://api.figshare.com/v1/pbl/oauth/access_token'

    redirect_response = request.get_full_path()
    oauth = OAuth1Session(client_key, client_secret=client_secret)
    oauth_response = oauth.parse_authorization_response(redirect_response)
    verifier = oauth_response.get('oauth_verifier')

    #Obtain Access Token
    oauth = OAuth1(client_key,
                   client_secret=client_secret,
                   resource_owner_key=request.session['resource_owner_key'],
                   resource_owner_secret=request.session['resource_owner_secret'],
                   verifier=verifier)

    r = requests.post(url=access_token_url, auth=oauth)
    credentials = parse_qs(r.content)
    tokens = {}
    tokens['owner_key'] = credentials[b'oauth_token'][0].decode("utf-8")
    tokens['owner_secret'] = credentials[b'oauth_token_secret'][0].decode("utf-8")
    Figshare_token().add_token(owner_key=tokens['owner_key'], owner_secret=tokens['owner_secret'])
    return tokens


def valid_tokens(tokens):

    oauth = OAuth1(client_key,
                  client_secret=client_secret,
                  resource_owner_key=tokens['owner_key'],
                  resource_owner_secret=tokens['owner_secret'],
                  signature_type='auth_header')
    url = 'http://api.figshare.com/v1/my_data/articles'
    client = requests.session()
    json_header = {'content-type': 'application/json'}
    response = client.get(url, auth=oauth, headers=json_header)
    if(response.status_code == 401):
        # probably invalid token
        return False
    return True

