# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web_copo', '0006_auto_20150213_1555'),
    ]

    operations = [
        migrations.AddField(
            model_name='enaexperiment',
            name='copo_exp_name',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
    ]
