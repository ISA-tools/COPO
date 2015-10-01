# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chunked_upload', '0003_remove_chunkedupload_hashed'),
    ]

    operations = [
        migrations.AddField(
            model_name='chunkedupload',
            name='hash',
            field=models.CharField(max_length=255, default=''),
            preserve_default=True,
        ),
    ]
