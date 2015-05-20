__author__ = 'felix.shaw@tgac.ac.uk - 14/05/15'
import jsonpickle

from apps.web_copo.mongo.figshare_da import *
import apps.web_copo.repos.figshare as f


def submit_to_figshare(request, article_id):
    #check status of figshare collection
    if FigshareCollection().is_clean(article_id):
        # there are no changes to the collection so don't submit
        out = HttpResponse()
        out.status_code = 304
        return out
    else:
        if (f.submit_to_figshare(article_id) == True):
            data = {'success': True}
            return HttpResponse(jsonpickle.encode(data))

