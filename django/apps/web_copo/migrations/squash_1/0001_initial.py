# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),

    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('type', models.CharField(default=b'custom submission', max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EnaExperiment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('instrument_model', models.CharField(max_length=50, null=True, blank=True)),
                ('library_name', models.CharField(max_length=50, null=True, blank=True)),
                ('library_source', models.CharField(max_length=50, null=True, blank=True)),
                ('library_selection', models.CharField(max_length=50, null=True, blank=True)),
                ('library_strategy', models.CharField(max_length=50, null=True, blank=True)),
                ('design_description', models.CharField(max_length=50, null=True, blank=True)),
                ('library_construction_protocol', models.CharField(max_length=50, null=True, blank=True)),
                ('library_layout', models.CharField(max_length=50, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EnaSample',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50, null=True, blank=True)),
                ('taxon_id', models.IntegerField()),
                ('common_name', models.CharField(max_length=50, null=True, blank=True)),
                ('anonymized_name', models.CharField(max_length=50, null=True, blank=True)),
                ('inividual_name', models.CharField(max_length=50, null=True, blank=True)),
                ('description', models.CharField(max_length=200, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EnaSampleAttr',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tag', models.CharField(max_length=50)),
                ('value', models.CharField(max_length=50)),
                ('units', models.CharField(max_length=50, null=True, blank=True)),
                ('ena_sample', models.ForeignKey(to='web_copo.EnaSample')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EnaStudy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('study_title', models.CharField(max_length=1000)),
                ('study_type', models.CharField(max_length=5000)),
                ('study_abstract', models.TextField(null=True, blank=True)),
                ('center_name', models.CharField(max_length=100, null=True, blank=True)),
                ('center_project_id', models.CharField(max_length=100, null=True, blank=True)),
                ('study_description', models.CharField(max_length=5000, null=True, blank=True)),
                ('collection', models.ForeignKey(to='web_copo.Collection')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EnaStudyAttr',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tag', models.CharField(max_length=50)),
                ('value', models.CharField(max_length=50)),
                ('unit', models.CharField(max_length=50, null=True, blank=True)),
                ('ena_study', models.ForeignKey(to='web_copo.EnaStudy')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=500)),
                ('abstract', models.TextField(null=True, blank=True)),
                ('abstract_short', models.CharField(max_length=150, null=True, blank=True)),
                ('date_created', models.DateField(default=datetime.date.today)),
                ('date_modified', models.DateField(default=datetime.date.today)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('URL', models.CharField(max_length=200, null=True, blank=True)),
                ('path', models.CharField(max_length=200, null=True, blank=True)),
                ('md5_checksum', models.CharField(max_length=200, null=True, blank=True)),
                ('collection', models.ForeignKey(to='web_copo.Collection')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='enasample',
            name='ena_study',
            field=models.ForeignKey(to='web_copo.EnaStudy'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='enaexperiment',
            name='data',
            field=models.ForeignKey(to='web_copo.Resource'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='enaexperiment',
            name='sample_reference',
            field=models.ForeignKey(to='web_copo.EnaStudy'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='collection',
            name='profile',
            field=models.ForeignKey(to='web_copo.Profile'),
            preserve_default=True,
        ),
    ]
