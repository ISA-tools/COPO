# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('web_copo', '0003_enasample_scientific_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='enasampleattr',
            old_name='units',
            new_name='unit',
        ),
    ]
