# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('web_copo', '0004_auto_20141127_1526'),
    ]

    operations = [
        migrations.RenameField(
            model_name='enasample',
            old_name='inividual_name',
            new_name='individual_name',
        ),
    ]
