# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Speaker.biography'
        db.add_column('meetups_speaker', 'biography',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Speaker.biography'
        db.delete_column('meetups_speaker', 'biography')


    models = {
        'meetups.meetup': {
            'Meta': {'object_name': 'Meetup', 'ordering': "['-date']"},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_ready': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True'}),
            'sponsors': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'sponsored_meetups'", 'blank': 'True', 'to': "orm['meetups.Sponsor']", 'symmetrical': 'False'}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'meetups'", 'blank': 'True', 'to': "orm['meetups.Venue']"})
        },
        'meetups.photo': {
            'Meta': {'object_name': 'Photo'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'meetup': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'photos'", 'to': "orm['meetups.Meetup']"})
        },
        'meetups.speaker': {
            'Meta': {'object_name': 'Speaker', 'ordering': "['first_name', 'last_name']"},
            'biography': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'meetups.sponsor': {
            'Meta': {'object_name': 'Sponsor', 'ordering': "['name']"},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'meetups.talk': {
            'Meta': {'object_name': 'Talk', 'ordering': "['order']"},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meetup': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'talks'", 'to': "orm['meetups.Meetup']"}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'slides_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'slides_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'speakers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'talks'", 'to': "orm['meetups.Speaker']", 'symmetrical': 'False'}),
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