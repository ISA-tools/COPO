# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import apps.chunked_upload.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ChunkedUpload',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('upload_id', models.CharField(editable=False, unique=True, default=apps.chunked_upload.models.generate_upload_id, max_length=32)),
                ('file', models.FileField(upload_to=apps.chunked_upload.models.generate_filename, max_length=255)),
                ('filename', models.CharField(max_length=255)),
                ('panel_id', models.IntegerField(default=1)),
                ('offset', models.PositiveIntegerField(default=0)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'Uploading'), (2, 'Complete'), (3, 'Failed')], default=1)),
                ('completed_on', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='chunked_uploads')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
