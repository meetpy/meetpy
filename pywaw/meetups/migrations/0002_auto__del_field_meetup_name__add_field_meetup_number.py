# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Meetup.name'
        db.delete_column('meetups_meetup', 'name')

        # Adding field 'Meetup.number'
        db.add_column('meetups_meetup', 'number',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=1, unique=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Meetup.name'
        db.add_column('meetups_meetup', 'name',
                      self.gf('django.db.models.fields.CharField')(max_length=100, default='Meetup'),
                      keep_default=False)

        # Deleting field 'Meetup.number'
        db.delete_column('meetups_meetup', 'number')


    models = {
        'meetups.meetup': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Meetup'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_ready': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True'}),
            'sponsors': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['meetups.Sponsor']", 'symmetrical': 'False', 'related_name': "'sponsored_meetups'"}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['meetups.Venue']", 'related_name': "'meetups'", 'null': 'True'})
        },
        'meetups.photo': {
            'Meta': {'object_name': 'Photo'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'meetup': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['meetups.Meetup']", 'related_name': "'photos'"})
        },
        'meetups.speaker': {
            'Meta': {'object_name': 'Speaker'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'max_length': '100'}),
            'website': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '200'})
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
            'Meta': {'ordering': "['time']", 'object_name': 'Talk'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meetup': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['meetups.Meetup']", 'related_name': "'talks'"}),
            'slides_file': ('django.db.models.fields.files.FileField', [], {'blank': 'True', 'max_length': '100'}),
            'slides_url': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '200'}),
            'speakers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['meetups.Speaker']", 'symmetrical': 'False', 'related_name': "'talks'"}),
            'time': ('django.db.models.fields.TimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'video_url': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '200'})
        },
        'meetups.venue': {
            'Meta': {'object_name': 'Venue'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '6'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '6'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['meetups']
