# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('web_copo', '0006_collection_typo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collection',
            name='typo',
        ),
    ]
