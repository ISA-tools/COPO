# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web_copo', '0019_auto_20150206_1422'),
    ]

    operations = [
        migrations.AddField(
            model_name='enaexperiment',
            name='panel_id',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
