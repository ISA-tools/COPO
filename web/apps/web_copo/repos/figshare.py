__author__ = 'felix.shaw@tgac.ac.uk - 29/04/15'

import json
import requests


client = requests.session()
json_header = {'content-type': 'application/json'}

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