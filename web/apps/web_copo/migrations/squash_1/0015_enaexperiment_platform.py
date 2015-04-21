# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web_copo', '0014_auto_20150205_1646'),
    ]

    operations = [
        migrations.AddField(
            model_name='enaexperiment',
            name='platform',
            field=models.CharField(max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
    ]
