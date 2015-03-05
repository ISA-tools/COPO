# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web_copo', '0016_enaexperiment_insert_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='enaexperiment',
            name='study',
            field=models.ForeignKey(to='web_copo.EnaStudy', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='enaexperiment',
            name='sample',
            field=models.ForeignKey(to='web_copo.EnaSample', null=True),
        ),
    ]
