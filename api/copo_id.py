__author__ = 'felix.shaw@tgac.ac.uk - 24/07/15'

import requests

import services


def get_uid():
    r = requests.get(services.WEB_SERVICES['COPO']['get_id'])
    print(r.text)
    return r.text