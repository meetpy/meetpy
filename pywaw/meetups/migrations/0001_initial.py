# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Sponsor'
        db.create_table('meetups_sponsor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('logo', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('meetups', ['Sponsor'])

        # Adding model 'Venue'
        db.create_table('meetups_venue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('longitude', self.gf('django.db.models.fields.DecimalField')(decimal_places=6, max_digits=9)),
            ('latitude', self.gf('django.db.models.fields.DecimalField')(decimal_places=6, max_digits=9)),
        ))
        db.send_create_signal('meetups', ['Venue'])

        # Adding model 'Meetup'
        db.create_table('meetups_meetup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('venue', self.gf('django.db.models.fields.related.ForeignKey')(null=True, related_name='meetups', blank=True, to=orm['meetups.Venue'])),
            ('is_ready', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('meetups', ['Meetup'])

        # Adding M2M table for field sponsors on 'Meetup'
        m2m_table_name = db.shorten_name('meetups_meetup_sponsors')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('meetup', models.ForeignKey(orm['meetups.meetup'], null=False)),
            ('sponsor', models.ForeignKey(orm['meetups.sponsor'], null=False))
        ))
        db.create_unique(m2m_table_name, ['meetup_id', 'sponsor_id'])

        # Adding model 'Speaker'
        db.create_table('meetups_speaker', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('meetups', ['Speaker'])

        # Adding model 'Talk'
        db.create_table('meetups_talk', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('meetup', self.gf('django.db.models.fields.related.ForeignKey')(related_name='talks', to=orm['meetups.Meetup'])),
            ('time', self.gf('django.db.models.fields.TimeField')()),
            ('slides_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
            ('slides_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('video_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('meetups', ['Talk'])

        # Adding M2M table for field speakers on 'Talk'
        m2m_table_name = db.shorten_name('meetups_talk_speakers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('talk', models.ForeignKey(orm['meetups.talk'], null=False)),
            ('speaker', models.ForeignKey(orm['meetups.speaker'], null=False))
        ))
        db.create_unique(m2m_table_name, ['talk_id', 'speaker_id'])

        # Adding model 'Photo'
        db.create_table('meetups_photo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('meetup', self.gf('django.db.models.fields.related.ForeignKey')(related_name='photos', to=orm['meetups.Meetup'])),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('meetups', ['Photo'])


    def backwards(self, orm):
        # Deleting model 'Sponsor'
        db.delete_table('meetups_sponsor')

        # Deleting model 'Venue'
        db.delete_table('meetups_venue')

        # Deleting model 'Meetup'
        db.delete_table('meetups_meetup')

        # Removing M2M table for field sponsors on 'Meetup'
        db.delete_table(db.shorten_name('meetups_meetup_sponsors'))

        # Deleting model 'Speaker'
        db.delete_table('meetups_speaker')

        # Deleting model 'Talk'
        db.delete_table('meetups_talk')

        # Removing M2M table for field speakers on 'Talk'
        db.delete_table(db.shorten_name('meetups_talk_speakers'))

        # Deleting model 'Photo'
        db.delete_table('meetups_photo')


    models = {
        'meetups.meetup': {
            'Meta': {'object_name': 'Meetup', 'ordering': "['-date']"},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_ready': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sponsors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['meetups.Sponsor']", 'related_name': "'sponsored_meetups'", 'blank': 'True', 'symmetrical': 'False'}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'meetups'", 'blank': 'True', 'to': "orm['meetups.Venue']"})
        },
        'meetups.photo': {
            'Meta': {'object_name': 'Photo'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'meetup': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'photos'", 'to': "orm['meetups.Meetup']"})
        },
        'meetups.speaker': {
            'Meta': {'object_name': 'Speaker'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'meetups.sponsor': {
            'Meta': {'object_name': 'Sponsor'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'meetups.talk': {
            'Meta': {'object_name': 'Talk', 'ordering': "['time']"},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meetup': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'talks'", 'to': "orm['meetups.Meetup']"}),
            'slides_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'slides_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'speakers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['meetups.Speaker']", 'related_name': "'talks'", 'symmetrical': 'False'}),
            'time': ('django.db.models.fields.TimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'video_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'meetups.venue': {
            'Meta': {'object_name': 'Venue'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'decimal_places': '6', 'max_digits': '9'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'decimal_places': '6', 'max_digits': '9'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['meetups']