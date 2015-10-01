# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chunked_upload', '0002_auto_20150923_1219'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chunkedupload',
            name='hashed',
        ),
    ]
