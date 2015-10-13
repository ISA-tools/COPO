# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import chunked_upload.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ChunkedUpload',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('upload_id', models.CharField(unique=True, max_length=32, default=chunked_upload.models.generate_upload_id, editable=False)),
                ('file', models.FileField(upload_to=chunked_upload.models.generate_filename, max_length=255)),
                ('filename', models.CharField(max_length=255)),
                ('hash', models.CharField(max_length=255, default='')),
                ('type', models.CharField(max_length=255, default='')),
                ('panel_id', models.IntegerField(default=1)),
                ('offset', models.PositiveIntegerField(default=0)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'Uploading'), (2, 'Complete'), (3, 'Failed')], default=1)),
                ('completed_on', models.DateTimeField(null=True, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='chunked_uploads')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
