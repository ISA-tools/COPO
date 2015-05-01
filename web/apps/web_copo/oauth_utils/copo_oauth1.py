__author__ = 'felix.shaw@tgac.ac.uk - 29/04/15'


from urllib.parse import parse_qs
from apps.web_copo.mongo.mongo_oauth_tokens import Figshare_token
import requests
from requests_oauthlib import OAuth1
from requests_oauthlib import OAuth1Session

client_key = 'id6JBVVeItadGDmjRUDljg'
client_secret = 'BC2tEMeCAT3veHhzfd2xIA'

def get_credentials():

    resource_owner_key = ''
    resource_owner_secret = ''
    tokens = None

    if (not Figshare_token().token_exists()):
        #if no token exists in the database
        tokens = get_token()
    else:
        #else retrieve saved tokens and validate
        tokens = Figshare_token().get_token_from_db()
        if(not valid_tokens(tokens)):
            Figshare_token().delete_old_token()
            tokens = get_token()

    resource_owner_key = tokens['owner_key']
    resource_owner_secret = tokens['owner_secret']
    return OAuth1(client_key,
                  client_secret=client_secret,
                  resource_owner_key=resource_owner_key,
                  resource_owner_secret=resource_owner_secret,
                  signature_type='auth_header')


def get_token():

    request_token_url = 'http://api.figshare.com/v1/pbl/oauth/request_token'
    authorization_url = 'http://api.figshare.com/v1/pbl/oauth/authorize'
    access_token_url = 'http://api.figshare.com/v1/pbl/oauth/access_token'

    #Obtain request token
    oauth = OAuth1Session(client_key, client_secret=client_secret)
    fetch_response = oauth.fetch_request_token(request_token_url)
    resource_owner_key = fetch_response.get('oauth_token')
    resource_owner_secret = fetch_response.get('oauth_token_secret')

    #Obtain Authorize Token
    authorize_url = authorization_url + '?oauth_token='
    authorize_url = authorize_url + resource_owner_key
    print('Please go here and authorize: ', authorize_url)
    redirect_response = input('Please input the verifier: ')
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
