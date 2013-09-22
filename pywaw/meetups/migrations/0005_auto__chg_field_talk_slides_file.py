# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Talk.slides_file'
        db.alter_column('meetups_talk', 'slides_file', self.gf('django.db.models.fields.files.FileField')(max_length=100))

    def backwards(self, orm):

        # Changing field 'Talk.slides_file'
        db.alter_column('meetups_talk', 'slides_file', self.gf('django.db.models.fields.files.FileField')(max_length=500))

    models = {
        'meetups.meetup': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Meetup'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_ready': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True'}),
            'sponsors': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['meetups.Sponsor']", 'related_name': "'sponsored_meetups'", 'blank': 'True'}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['meetups.Venue']", 'related_name': "'meetups'", 'blank': 'True'})
        },
        'meetups.photo': {
            'Meta': {'object_name': 'Photo'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'meetup': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['meetups.Meetup']", 'related_name': "'photos'"})
        },
        'meetups.speaker': {
            'Meta': {'ordering': "['first_name', 'last_name']", 'object_name': 'Speaker'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'meetups.sponsor': {
            'Meta': {'ordering': "['name']", 'object_name': 'Sponsor'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'meetups.talk': {
            'Meta': {'ordering': "['order']", 'object_name': 'Talk'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meetup': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['meetups.Meetup']", 'related_name': "'talks'"}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'slides_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'slides_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'speakers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['meetups.Speaker']", 'related_name': "'talks'"}),
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