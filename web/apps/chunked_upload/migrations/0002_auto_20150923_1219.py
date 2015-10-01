# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chunked_upload', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chunkedupload',
            name='hashed',
            field=models.CharField(default=None, max_length=255),
            preserve_default=True,
        ),
    ]
