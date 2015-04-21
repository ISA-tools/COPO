# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web_copo', '0017_auto_20150206_1114'),
    ]

    operations = [
        migrations.RenameField(
            model_name='expfile',
            old_name='experiment_id',
            new_name='experiment',
        ),
        migrations.RenameField(
            model_name='expfile',
            old_name='file_id',
            new_name='file',
        ),
    ]
