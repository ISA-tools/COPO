# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    replaces = [(b'web_copo', '0001_initial'), (b'web_copo', '0002_auto_20141124_1710'), (b'web_copo', '0003_enasample_scientific_name'), (b'web_copo', '0004_auto_20141127_1526'), (b'web_copo', '0005_auto_20141201_1111'), (b'web_copo', '0006_collection_typo'), (b'web_copo', '0007_remove_collection_typo'), (b'web_copo', '0008_document'), (b'web_copo', '0009_auto_20141209_1210'), (b'web_copo', '0010_auto_20141209_1405'), (b'web_copo', '0011_auto_20141215_1454'), (b'web_copo', '0012_expfile'), (b'web_copo', '0013_expfile_md5_hash'), (b'web_copo', '0014_auto_20150205_1646'), (b'web_copo', '0015_enaexperiment_platform'), (b'web_copo', '0016_enaexperiment_insert_size'), (b'web_copo', '0017_auto_20150206_1114'), (b'web_copo', '0018_auto_20150206_1219'), (b'web_copo', '0019_auto_20150206_1422'), (b'web_copo', '0020_enaexperiment_panel_id')]

    dependencies = [
        ('chunked_upload', '0001_initial'),
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
                ('unit', models.CharField(max_length=50, null=True, blank=True)),
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
        migrations.RenameField(
            model_name='enastudy',
            old_name='center_project_id',
            new_name='center_project_name',
        ),
        migrations.AddField(
            model_name='enasample',
            name='scientific_name',
            field=models.CharField(max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.RenameField(
            model_name='enasample',
            old_name='inividual_name',
            new_name='individual_name',
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('docfile', models.FileField(upload_to=b'/Users/fshaw/Desktop/test')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ExpFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('experiment', models.ForeignKey(to='web_copo.EnaExperiment')),
                ('file', models.ForeignKey(to='chunked_upload.ChunkedUpload')),
                ('md5_hash', models.CharField(max_length=50, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
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
        migrations.AddField(
            model_name='enaexperiment',
            name='platform',
            field=models.CharField(max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='enaexperiment',
            name='insert_size',
            field=models.IntegerField(default=0, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='enaexperiment',
            name='study',
            field=models.ForeignKey(to='web_copo.EnaStudy', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='enaexperiment',
            name='sample',
            field=models.ForeignKey(to='web_copo.EnaSample', null=True),
        ),
        migrations.AddField(
            model_name='enaexperiment',
            name='panel_id',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
