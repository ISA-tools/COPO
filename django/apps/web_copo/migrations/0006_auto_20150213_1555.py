# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web_copo', '0005_enaexperiment_data_modal_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expfile',
            name='file',
            field=models.OneToOneField(to='chunked_upload.ChunkedUpload'),
        ),
    ]
