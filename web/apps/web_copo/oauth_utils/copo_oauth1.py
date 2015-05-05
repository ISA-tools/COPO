__author__ = 'felix.shaw@tgac.ac.uk - 29/04/15'

from urllib.parse import parse_qs

import requests
from requests_oauthlib import OAuth1
from requests_oauthlib import OAuth1Session
from django.http import HttpResponseRedirect
from django_tools.middlewares import ThreadLocal

from apps.web_copo.mongo.mongo_oauth_tokens import Figshare_token


client_key = 'id6JBVVeItadGDmjRUDljg'
client_secret = 'BC2tEMeCAT3veHhzfd2xIA'
resource_owner_key = ''
resource_owner_secret = ''
tokens = None


def get_credentials():
    if (not Figshare_token().token_exists()):
        #if no token exists in the database
        tokens = get_authorize_url()
    else:
        #else retrieve saved tokens and validate
        tokens = Figshare_token().get_token_from_db()
        if(not valid_tokens(tokens)):
            Figshare_token().delete_old_token()
            tokens = get_authorize_url()

    resource_owner_key = tokens['owner_key']
    resource_owner_secret = tokens['owner_secret']
    return OAuth1(client_key,
                  client_secret=client_secret,
                  resource_owner_key=resource_owner_key,
                  resource_owner_secret=resource_owner_secret,
                  signature_type='auth_header')


def get_authorize_url():

    request_token_url = 'http://api.figshare.com/v1/pbl/oauth/request_token'
    authorization_url = 'http://api.figshare.com/v1/pbl/oauth/authorize'


    #Obtain request token
    request = ThreadLocal.get_current_request()

    oauth = OAuth1Session(client_key, client_secret=client_secret, callback_uri=request.build_absolute_uri())
    fetch_response = oauth.fetch_request_token(request_token_url)
    resource_owner_key = fetch_response.get('oauth_token')
    resource_owner_secret = fetch_response.get('oauth_token_secret')

    #Obtain Authorize Token
    authorize_url = authorization_url + '?oauth_token='
    authorize_url = authorize_url + resource_owner_key

    #redirect user to login page
    return authorize_url


def redirect_to_service(authorize_url):
    HttpResponseRedirect(authorize_url)


def get_access_token(request):

    access_token_url = 'http://api.figshare.com/v1/pbl/oauth/access_token'

    redirect_response = request.url
    oauth = OAuth1Session(client_key, client_secret=client_secret)
    oauth_response = oauth.parse_authorization_response(redirect_response)
    verifier = oauth_response.get('oauth_verifier')

    #Obtain Access Token
    oauth = OAuth1(client_key,
                   client_secret=client_secret,
                   resource_owner_key=resource_owner_key,
                   resource_owner_secret=resource_owner_secret,
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
