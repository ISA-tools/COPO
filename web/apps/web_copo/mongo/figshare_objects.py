__author__ = 'felix.shaw@tgac.ac.uk - 11/05/15'

from django.http import HttpResponse
import jsonpickle

from apps.web_copo.mongo.mongo_util import *
from apps.web_copo.mongo.resource import *


FigshareFiles = get_collection_ref("Figshare_Files")
Collection_Heads = get_collection_ref("Collection_Heads")

class FigshareCollection(Resource):

    def add_figshare(self, values):
        return FigshareFiles.insert(values)

    def save_article(self, request):
        # make new entries for collection
        input_files = request.POST.getlist('files[]')
        tags = request.POST.getlist('tags[]')
        # add tags to existing files
        for f in input_files:
            FigshareFiles.update(
            {'_id': ObjectId(f)},
            {'$push':
                 {"tags": tags}
            }
        )



        # now push list of files to the collection
        collection_id = request.session['collection_id']
        for f in input_files:
            Collection_Heads.update(
                {'_id': ObjectId(collection_id)},
                {'$push':
                     {"collection_details": ObjectId(f)}
                }
            )


        return HttpResponse(jsonpickle.encode('HERE WE GO!'))

