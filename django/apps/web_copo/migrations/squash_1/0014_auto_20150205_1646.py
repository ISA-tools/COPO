# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web_copo', '0013_expfile_md5_hash'),
    ]

    operations = [
        migrations.RenameField(
            model_name='enaexperiment',
            old_name='instrument_model',
            new_name='instrument',
        ),
        migrations.RenameField(
            model_name='enaexperiment',
            old_name='library_construction_protocol',
            new_name='lib_construction_protocol',
        ),
        migrations.RenameField(
            model_name='enaexperiment',
            old_name='library_layout',
            new_name='lib_layout',
        ),
        migrations.RenameField(
            model_name='enaexperiment',
            old_name='library_selection',
            new_name='lib_selection',
        ),
        migrations.RenameField(
            model_name='enaexperiment',
            old_name='library_source',
            new_name='lib_source',
        ),
        migrations.RenameField(
            model_name='enaexperiment',
            old_name='library_strategy',
            new_name='lib_strategy',
        ),
        migrations.RenameField(
            model_name='enaexperiment',
            old_name='sample_reference',
            new_name='sample',
        ),
        migrations.RemoveField(
            model_name='enaexperiment',
            name='data',
        ),
        migrations.RemoveField(
            model_name='enaexperiment',
            name='library_name',
        ),
        migrations.AddField(
            model_name='enaexperiment',
            name='file_type',
            field=models.CharField(max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='enaexperiment',
            name='lib_name',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
    ]
