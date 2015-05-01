__author__ = 'felix.shaw@tgac.ac.uk - 29/04/15'


from urllib.parse import parse_qs
from apps.web_copo.oauth_utils im
import requests
from requests_oauthlib import OAuth1
from requests_oauthlib import OAuth1Session


def get_credentials():
    client_key = 'id6JBVVeItadGDmjRUDljg'
    client_secret = 'BC2tEMeCAT3veHhzfd2xIA'

    #resource_owner_key = 'BskboZgzVXwcwX9xgv7puwkvKqJev8yklxzg55AaFKDwXskboZgzVXwcwX9xgv7puw'
    #resource_owner_secret = 'eBp6Hc0JhynZSPtGDGFRTw'



    # TODO - here we put check logic to see if user has granted COPO access to the figshare account
    if (resource_owner_key == '' or resource_owner_secret == ''):
        request_token_url = 'http://api.figshare.com/v1/pbl/oauth_utils/request_token'
        authorization_url = 'http://api.figshare.com/v1/pbl/oauth_utils/authorize'
        access_token_url = 'http://api.figshare.com/v1/pbl/oauth_utils/access_token'

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
        resource_owner_key = credentials[b'oauth_token'][0].decode("utf-8")
        resource_owner_secret = credentials[b'oauth_token_secret'][0].decode("utf-8")

        print(resource_owner_key)
        print(resource_owner_secret)

    return OAuth1(client_key,
                  client_secret=client_secret,
                  resource_owner_key=resource_owner_key,
                  resource_owner_secret=resource_owner_secret,
                  signature_type='auth_header')

