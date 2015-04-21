# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chunked_upload', '0001_initial'),
        ('web_copo', '0011_auto_20141215_1454'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('experiment_id', models.ForeignKey(to='web_copo.EnaExperiment')),
                ('file_id', models.ForeignKey(to='chunked_upload.ChunkedUpload')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
