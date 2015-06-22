__author__ = 'felix.shaw@tgac.ac.uk - 14/05/15'

from apps.web_copo.mongo.figshare_da import *
import apps.web_copo.repos.figshare as f


def submit_to_figshare(request, article_id):
    # check status of figshare collection
    if FigshareCollection().is_clean(article_id):
        # there are no changes to the collection so don't submit
        data = {'success': False}
        return HttpResponse(jsonpickle.encode(data))
    else:
        # get collection_details
        details = FigshareCollection().get_collection_details_from_collection_head(article_id)
        for d in details['collection_details']:
            figshare_article_id = f.submit_to_figshare(d)
            if (figshare_article_id != None):
                # figshare_article_id is the Figshare article id
                FigshareCollection().mark_as_clean(article_id)
                data = {'success': True}
        return HttpResponse(jsonpickle.encode(data))


def view_in_figshare(request, article_id):
    url = FigshareCollection().get_url(article_id)
    return HttpResponse(jsonpickle.encode(url))


def delete_from_figshare(request, article_id):
    if (f.delete_from_figshare(article_id)):
        FigshareCollection().delete_article(request)

        data = {'success': True}
    else:
        data = {'success': False}
    return HttpResponse(jsonpickle.encode(data))
