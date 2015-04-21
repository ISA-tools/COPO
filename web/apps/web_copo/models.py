from django.db import models
from django.contrib.auth.models import User
from time import time




def get_upload_file_name(instance, filename):
    return 'uploaded_files/%s_%s' % (str(time()).replace('.', '_'), filename)


class RepositoryFeedback(models.Model):
    current_pct = models.CharField(max_length=128)
    session_key = models.CharField(max_length=128)
