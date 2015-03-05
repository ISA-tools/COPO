# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('web_copo', '0002_auto_20141124_1710'),
    ]

    operations = [
        migrations.AddField(
            model_name='enasample',
            name='scientific_name',
            field=models.CharField(max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
    ]
