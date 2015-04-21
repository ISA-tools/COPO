# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chunked_upload', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('type', models.CharField(default='custom submission', max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('docfile', models.FileField(upload_to='/Users/fshaw/Desktop/test')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EnaExperiment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('platform', models.CharField(max_length=50, blank=True, null=True)),
                ('instrument', models.CharField(max_length=50, blank=True, null=True)),
                ('lib_source', models.CharField(max_length=50, blank=True, null=True)),
                ('lib_selection', models.CharField(max_length=50, blank=True, null=True)),
                ('lib_strategy', models.CharField(max_length=50, blank=True, null=True)),
                ('insert_size', models.IntegerField(blank=True, default=0, null=True)),
                ('design_description', models.CharField(max_length=50, blank=True, null=True)),
                ('lib_construction_protocol', models.CharField(max_length=50, blank=True, null=True)),
                ('lib_layout', models.CharField(max_length=50, blank=True, null=True)),
                ('file_type', models.CharField(max_length=50, blank=True, null=True)),
                ('lib_name', models.CharField(max_length=100, blank=True, null=True)),
                ('panel_ordering', models.IntegerField(default=0)),
                ('panel_id', models.CharField(max_length=100, blank=True, null=True)),
                ('data_modal_id', models.CharField(max_length=100, blank=True, null=True)),
                ('copo_exp_name', models.CharField(max_length=100, blank=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EnaSample',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=50, blank=True, null=True)),
                ('taxon_id', models.IntegerField()),
                ('scientific_name', models.CharField(max_length=50, blank=True, null=True)),
                ('common_name', models.CharField(max_length=50, blank=True, null=True)),
                ('anonymized_name', models.CharField(max_length=50, blank=True, null=True)),
                ('individual_name', models.CharField(max_length=50, blank=True, null=True)),
                ('description', models.CharField(max_length=200, blank=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EnaSampleAttr',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('tag', models.CharField(max_length=50)),
                ('value', models.CharField(max_length=50)),
                ('unit', models.CharField(max_length=50, blank=True, null=True)),
                ('ena_sample', models.ForeignKey(to='web_copo.EnaSample')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EnaStudy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('study_title', models.CharField(max_length=1000)),
                ('study_type', models.CharField(max_length=5000)),
                ('study_abstract', models.TextField(blank=True, null=True)),
                ('center_name', models.CharField(max_length=100, blank=True, null=True)),
                ('center_project_name', models.CharField(max_length=100, blank=True, null=True)),
                ('study_description', models.CharField(max_length=5000, blank=True, null=True)),
                ('collection', models.ForeignKey(to='web_copo.Collection')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EnaStudyAttr',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('tag', models.CharField(max_length=50)),
                ('value', models.CharField(max_length=50)),
                ('unit', models.CharField(max_length=50, blank=True, null=True)),
                ('ena_study', models.ForeignKey(to='web_copo.EnaStudy')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ExpFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('md5_hash', models.CharField(max_length=50, blank=True, null=True)),
                ('experiment', models.ForeignKey(to='web_copo.EnaExperiment')),
                ('file', models.OneToOneField(to='chunked_upload.ChunkedUpload')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=500)),
                ('abstract', models.TextField(blank=True, null=True)),
                ('abstract_short', models.CharField(max_length=150, blank=True, null=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('URL', models.CharField(max_length=200, blank=True, null=True)),
                ('path', models.CharField(max_length=200, blank=True, null=True)),
                ('md5_checksum', models.CharField(max_length=200, blank=True, null=True)),
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
            name='sample',
            field=models.ForeignKey(to='web_copo.EnaSample', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='enaexperiment',
            name='study',
            field=models.ForeignKey(to='web_copo.EnaStudy', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='collection',
            name='profile',
            field=models.ForeignKey(to='web_copo.Profile'),
            preserve_default=True,
        ),
    ]
