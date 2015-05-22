__author__ = 'felix.shaw@tgac.ac.uk - 14/05/15'

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
        figshare_article_id = f.submit_to_figshare(article_id)
        if (figshare_article_id != None):
            # figshare_article_id is the Figshare article id
            FigshareCollection().mark_as_clean(article_id)
            data = {'success': True}
            return HttpResponse(jsonpickle.encode(data))

def delete_from_figshare(request, article_id):

    if (f.delete_from_figshare(article_id)):
        FigshareCollection().delete_article(request)

        data = {'success': True}
    else:
        data = {'success': False}
    return HttpResponse(jsonpickle.encode(data))


