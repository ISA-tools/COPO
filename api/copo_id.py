__author__ = 'felix.shaw@tgac.ac.uk - 24/07/15'

import requests

from services import WEB_SERVICES


def get_uid():
    r = requests.get(WEB_SERVICES['COPO']['get_id'])
    print(r.text)
    return r.text