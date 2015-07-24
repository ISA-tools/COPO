__author__ = 'felix.shaw@tgac.ac.uk - 11/05/15'

from django_tools.middlewares import ThreadLocal
from django.http import HttpResponse
from django.utils import timezone
import jsonpickle

from web_copo.mongo.resource import *
from web_copo.mongo.mongo_util import *
from chunked_upload.models import generate_upload_id
from settings.settings import *

FigshareTokens = get_collection_ref("Figshare_tokens")
FigshareCollections = get_collection_ref("Figshare_Files")
Collection_Heads = get_collection_ref("Collection_Heads")


class FigshareCollection(Resource):
    def receive_data_file(request):
        # need to make a chunked upload record to store details of the file
        if request.method == 'POST':
            f = request.FILES['file']
            repo_type = request.POST['repo']
            # for t in request.POST['tags']:
            # tags.append(t)
            filename = generate_upload_id() + '.part'
            destination = open(os.path.join(settings.MEDIA_ROOT, filename), 'wb+')
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()

            user = request.user
            fname = f.__str__()
            attrs = {'user':
                {
                    'id': user.id,
                    'username': user.username,
                    'firstname': user.first_name,
                    'lastname': user.last_name,
                    'email': user.email
                },
                'original_name': fname,
                'uploaded_on': timezone.now(),
                'offset': f.size,
                'hashed_name': filename,
                'path': settings.MEDIA_ROOT,
            }

            if repo_type == 'figshare':
                file_id = FigshareCollection().add_figshare(attrs)


            # create output structure to pass back to jquery-upload
            files = []
            file = {}
            file['name'] = f._name

            file['size'] = f.size / (1000 * 1000.0)
            file['id'] = str(file_id)
            file['url'] = ''
            file['thumbnailUrl'] = ''
            file['deleteUrl'] = ''
            file['deleteType'] = 'DELETE'
            files.append(file)

            out = jsonpickle.encode(files)

        return HttpResponse(out, content_type='json')

    # method to get the containing collection head for a given article id
    def get_collection_head_from_article(self, collection_id):
        return Collection_Heads.find_one({'collection_details': {'$in': [ObjectId(collection_id)]}})

    def add_figshare_accession_to_article(self, figshare_id=0, article_id=0):
        return FigshareCollections.update({'_id': ObjectId(article_id)},
                                          {'$set': {'figshare_accession': figshare_id}})

    def add_figshare_url_to_article(self, figshare_id=0, article_id=0):
        figshare_url = 'http://figshare.com/preview/_preview/' + str(figshare_id)
        return FigshareCollections.update({'_id': ObjectId(article_id)},
                                          {'$set': {'figshare_url': figshare_url}})
    def get_url(self, article_id):
        return FigshareCollections.find_one({'_id': ObjectId(article_id)}, {'figshare_url': 1})

    # called from jquery upload handler to add new file details
    def add_figshare(self, values):
        return FigshareCollections.insert(values)

    def get_figshare_id(self, article_id):
        return FigshareCollections.find_one({'_id': ObjectId(article_id)},
                                            {'_id': 0, 'figshare_accession': 1})

    # method to check whether the specified collection has changes needed to be uploaded
    def is_clean(self, collection_id):
        collection_head = Collection_Heads.find_one({'_id': ObjectId(collection_id)})
        return collection_head['is_clean']

    # Collection head stores high level meta about the collection, the details contain the
    # fine grained detail relating to the individual collection type
    def get_collection_details_from_collection_head(self, collection_head_id):
        return Collection_Heads.find_one({'_id': ObjectId(collection_head_id)},
                                         {'collection_details': 1})

    # method to mark a collection as clean
    def mark_as_clean(self, collection_id):

        Collection_Heads.update({'_id': ObjectId(collection_id)},
                                {'$set': {'is_clean': True}})

    # method called from article view handler to create table of articles in the specified collection
    def get_articles_in_collection(self, collection_id):

        articles = []
        article_ids = Collection_Heads.find(
            {'_id': ObjectId(collection_id),
             'collection_details': {
                 '$exists': 'true'
             }},
            {"collection_details": 1, "_id": 0})
        if article_ids.count() > 0:
            article_ids = list(article_ids)[0]['collection_details']
            articles = FigshareCollections.find({
                "_id": {
                    "$in": article_ids
                }
            },
                {
                    'original_name': 1,
                    'uploaded_on': 1,
                    'offset': 1
                }
            )

        return list(articles)

    # method called insert article ids int collection head
    def save_article(self, request):
        # make new entries for collection
        input_files = request.POST.getlist('files[]')
        tags = request.POST.getlist('tags[]')
        article_type = request.POST.get("article_type")
        description = request.POST.get("description")
        # add tags to existing files
        out = []
        for f in input_files:
            update = FigshareCollections.find_one({'_id': ObjectId(f)},
                                                  {'original_name': 1, 'uploaded_on': 1, 'offset': 1})
            update["id"] = str(update["_id"])
            update["uploaded_on"] = update["uploaded_on"].strftime('%b %d, %Y, %I:%M %p')
            out.append(update)
            for t in tags:
                FigshareCollections.update(
                    {'_id': ObjectId(f)},
                    {'$push':
                         {"tags": t}
                     }
                )
            FigshareCollections.update(
                {'_id': ObjectId(f)},
                {"$set":
                     {"article_type": article_type, "description": description}}
            )
        # now push list of files to the collection
        collection_id = request.session['collection_id']
        for f in input_files:
            Collection_Heads.update(
                {'_id': ObjectId(collection_id)},
                {
                    '$push':
                        {"collection_details": ObjectId(f)},
                    '$set':
                        {"is_clean": False}
                }

            )

        return HttpResponse(jsonpickle.encode(out))

    # called from front-end to delete article
    def delete_article(self, request):
        id = request.POST['article_id']
        # delete Figshare collection entry
        obj = ObjectId(id)
        # pull id from collection head
        collection_id = request.session["collection_id"]
        Collection_Heads.update(
            {'_id': ObjectId(collection_id)},
            {'$pull':
                 {'collection_details': obj}
             }
        )
        FigshareCollections.remove({"_id": obj})
        out = {}
        out['success'] = True
        return HttpResponse(jsonpickle.encode(out))

    def get_article(self, article_id):
        return FigshareCollections.find_one({'_id': ObjectId(article_id)})


class Figshare_token(Resource):
    def token_exists(self):
        user = ThreadLocal.get_current_user()
        return (FigshareTokens.find({'user_id': user.id}).limit(1).count() > 0)

    def delete_old_token(self):
        user = ThreadLocal.get_current_user()
        FigshareTokens.delete_many({'user_id': user.id})

    def get_token_from_db(self):
        user = ThreadLocal.get_current_user()
        return FigshareTokens.find_one({'user_id': user.id})

    def add_token(self, owner_key=None, owner_secret=None):
        user = ThreadLocal.get_current_user()
        FigshareTokens.insert({'user_id': user.id, 'owner_key': owner_key, 'owner_secret': owner_secret})
