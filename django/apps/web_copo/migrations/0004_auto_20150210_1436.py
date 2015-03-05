# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web_copo', '0003_enaexperiment_panel_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='enaexperiment',
            old_name='ordering_id',
            new_name='panel_ordering',
        ),
    ]
