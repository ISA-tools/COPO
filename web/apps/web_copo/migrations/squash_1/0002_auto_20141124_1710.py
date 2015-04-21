# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('web_copo', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='enastudy',
            old_name='center_project_id',
            new_name='center_project_name',
        ),
    ]
