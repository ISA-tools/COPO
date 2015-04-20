# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web_copo', '0002_auto_20150210_1428'),
    ]

    operations = [
        migrations.AddField(
            model_name='enaexperiment',
            name='panel_id',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
    ]
