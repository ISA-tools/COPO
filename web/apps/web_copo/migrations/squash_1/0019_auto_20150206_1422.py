# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web_copo', '0018_auto_20150206_1219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enaexperiment',
            name='insert_size',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
    ]
