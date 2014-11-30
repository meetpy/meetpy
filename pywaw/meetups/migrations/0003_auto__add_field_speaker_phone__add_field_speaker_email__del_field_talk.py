# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Speaker.phone'
        db.add_column('meetups_speaker', 'phone',
                      self.gf('django.db.models.fields.CharField')(blank=True, default='', max_length=30),
                      keep_default=False)

        # Adding field 'Speaker.email'
        db.add_column('meetups_speaker', 'email',
                      self.gf('django.db.models.fields.EmailField')(blank=True, default='', max_length=75),
                      keep_default=False)

        # Deleting field 'Talk.time'
        db.delete_column('meetups_talk', 'time')

        # Adding field 'Talk.order'
        db.add_column('meetups_talk', 'order',
                      self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Speaker.phone'
        db.delete_column('meetups_speaker', 'phone')

        # Deleting field 'Speaker.email'
        db.delete_column('meetups_speaker', 'email')


        # User chose to not deal with backwards NULL issues for 'Talk.time'
        raise RuntimeError("Cannot reverse this migration. 'Talk.time' and its values cannot be restored.")
        # Deleting field 'Talk.order'
        db.delete_column('meetups_talk', 'order')


    models = {
        'meetups.meetup': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Meetup'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_ready': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True'}),
            'sponsors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['meetups.Sponsor']", 'blank': 'True', 'symmetrical': 'False', 'related_name': "'sponsored_meetups'"}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['meetups.Venue']", 'null': 'True', 'related_name': "'meetups'"})
        },
        'meetups.photo': {
            'Meta': {'object_name': 'Photo'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'meetup': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['meetups.Meetup']", 'related_name': "'photos'"})
        },
        'meetups.speaker': {
            'Meta': {'ordering': "['first_name', 'last_name']", 'object_name': 'Speaker'},
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'phone': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'max_length': '100'}),
            'website': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '200'})
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
            'slides_file': ('django.db.models.fields.files.FileField', [], {'blank': 'True', 'max_length': '100'}),
            'slides_url': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '200'}),
            'speakers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['meetups.Speaker']", 'symmetrical': 'False', 'related_name': "'talks'"}),
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