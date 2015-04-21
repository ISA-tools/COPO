# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web_copo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RepositoryFeedback',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('current_pct', models.CharField(max_length=128)),
                ('session_key', models.CharField(max_length=128)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='collection',
            name='profile',
        ),
        migrations.DeleteModel(
            name='Document',
        ),
        migrations.RemoveField(
            model_name='enaexperiment',
            name='sample',
        ),
        migrations.RemoveField(
            model_name='enaexperiment',
            name='study',
        ),
        migrations.RemoveField(
            model_name='enasample',
            name='ena_study',
        ),
        migrations.RemoveField(
            model_name='enasampleattr',
            name='ena_sample',
        ),
        migrations.DeleteModel(
            name='EnaSample',
        ),
        migrations.DeleteModel(
            name='EnaSampleAttr',
        ),
        migrations.RemoveField(
            model_name='enastudy',
            name='collection',
        ),
        migrations.RemoveField(
            model_name='enastudyattr',
            name='ena_study',
        ),
        migrations.DeleteModel(
            name='EnaStudy',
        ),
        migrations.DeleteModel(
            name='EnaStudyAttr',
        ),
        migrations.RemoveField(
            model_name='expfile',
            name='experiment',
        ),
        migrations.DeleteModel(
            name='EnaExperiment',
        ),
        migrations.RemoveField(
            model_name='expfile',
            name='file',
        ),
        migrations.DeleteModel(
            name='ExpFile',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
        migrations.RemoveField(
            model_name='resource',
            name='collection',
        ),
        migrations.DeleteModel(
            name='Collection',
        ),
        migrations.DeleteModel(
            name='Resource',
        ),
    ]
