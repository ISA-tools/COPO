# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.files.storage


class Migration(migrations.Migration):
    dependencies = [
        ('web_copo', '0009_auto_20141209_1210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='docfile',
            field=models.FileField(
                storage=django.core.files.storage.FileSystemStorage(location=b' /Users/fshaw/Desktop/test'),
                upload_to=b''),
        ),
    ]
