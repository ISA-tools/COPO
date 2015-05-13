__author__ = 'felix.shaw@tgac.ac.uk - 08/05/15'

from django.http import HttpResponse
from django.utils import timezone
import jsonpickle

from apps.web_copo.mongo.figshare_objects import FigshareCollection
from apps.chunked_upload.models import generate_upload_id
from project_copo.settings.settings import *


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
                 'path': settings.UPLOAD_PATH,
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