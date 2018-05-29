# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

import misc.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('url', models.URLField()),
                ('logo', models.ImageField(upload_to=misc.models.SlugifyUploadTo('partners', ['name']))),
                ('is_public', models.BooleanField()),
            ],
        ),
    ]
