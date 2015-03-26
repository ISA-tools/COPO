# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web_copo', '0001_squashed_0020_enaexperiment_panel_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='enaexperiment',
            old_name='panel_id',
            new_name='ordering_id',
        ),
    ]
