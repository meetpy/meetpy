# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import misc.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExternalLink',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('url', models.URLField()),
                ('type', models.CharField(max_length=10, choices=[('photos', 'Photos'), ('article', 'Article'), ('other', 'Other')])),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Meetup',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('number', models.PositiveIntegerField(unique=True)),
                ('date', models.DateTimeField()),
                ('is_ready', models.BooleanField(default=False)),
                ('date_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Speaker',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('website', models.URLField(blank=True)),
                ('photo', models.ImageField(upload_to=misc.models.SlugifyUploadTo('speakers', ['first_name', 'last_name']), blank=True)),
                ('phone', models.CharField(max_length=30, blank=True)),
                ('email', models.EmailField(max_length=254, blank=True)),
                ('biography', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['first_name', 'last_name'],
            },
        ),
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('website', models.URLField()),
                ('logo', models.ImageField(upload_to='sponsors')),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Talk',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=1000)),
                ('description', models.TextField(blank=True)),
                ('order', models.PositiveSmallIntegerField(null=True)),
                ('slides_file', models.FileField(max_length=500, upload_to=misc.models.SlugifyUploadTo('slides', ['meetup', 'title']), blank=True)),
                ('slides_url', models.URLField(blank=True)),
                ('video_url', models.URLField(blank=True)),
                ('language', models.CharField(default='pl', choices=[('pl', 'Polish'), ('en', 'English')], max_length=2)),
                ('meetup', models.ForeignKey(null=True, to='meetups.Meetup', related_name='talks', blank=True)),
                ('speakers', models.ManyToManyField(to='meetups.Speaker', related_name='talks')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='TalkProposal',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('message', models.TextField(blank=True)),
                ('date_submitted', models.DateTimeField(auto_now_add=True)),
                ('talk', models.ForeignKey(to='meetups.Talk')),
            ],
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=200)),
                ('longitude', models.DecimalField(max_digits=9, decimal_places=6)),
                ('latitude', models.DecimalField(max_digits=9, decimal_places=6)),
            ],
        ),
        migrations.AddField(
            model_name='meetup',
            name='sponsors',
            field=models.ManyToManyField(to='meetups.Sponsor', blank=True, related_name='sponsored_meetups'),
        ),
        migrations.AddField(
            model_name='meetup',
            name='venue',
            field=models.ForeignKey(null=True, to='meetups.Venue', related_name='meetups', blank=True),
        ),
        migrations.AddField(
            model_name='externallink',
            name='meetup',
            field=models.ForeignKey(to='meetups.Meetup', related_name='external_links'),
        ),
    ]
