__author__ = 'felix.shaw@tgac.ac.uk - 08/05/15'

from django.http import HttpResponse
from django.utils import timezone
import jsonpickle

from apps.chunked_upload.models import generate_upload_id
from project_copo.settings.settings import *


def receive_data_file(request):

    # need to make a chunked upload record to store deails of the file
    if request.method == 'POST':
        tags = []
        #for t in request.POST['tags']:
        #    tags.append(t)

        f = request.FILES['file']
        user = request.user
        fname = f.__str__()
        attrs = {'user': request.user,
                 'original_name': fname,
                 'uploaded_on': timezone.now(),
                 'offset': f.size,
                 'hashed_name': generate_upload_id(),
                 'path': settings.UPLOAD_PATH,
                 'user_id': user.id,
                 'tags': tags}



        # create output structure to pass back to jquery-upload
        files = {}
        files['files'] = {}
        files['files']['name'] = f._name

        files['files']['size'] = f.size / (1000 * 1000.0)
        files['files']['id'] = 20
        files['files']['url'] = ''
        files['files']['thumbnailUrl'] = ''
        files['files']['deleteUrl'] = ''
        files['files']['deleteType'] = 'DELETE'

        str = jsonpickle.encode(files)
    return HttpResponse(str, content_type='json')