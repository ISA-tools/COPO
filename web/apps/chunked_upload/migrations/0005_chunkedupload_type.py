# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chunked_upload', '0004_chunkedupload_hash'),
    ]

    operations = [
        migrations.AddField(
            model_name='chunkedupload',
            name='type',
            field=models.CharField(default='', max_length=255),
            preserve_default=True,
        ),
    ]
