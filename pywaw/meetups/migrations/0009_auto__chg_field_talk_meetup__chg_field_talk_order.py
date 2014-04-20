# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Talk.meetup'
        db.alter_column('meetups_talk', 'meetup_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['meetups.Meetup']))

        # Changing field 'Talk.order'
        db.alter_column('meetups_talk', 'order', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Talk.meetup'
        raise RuntimeError("Cannot reverse this migration. 'Talk.meetup' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Talk.meetup'
        db.alter_column('meetups_talk', 'meetup_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['meetups.Meetup']))

        # User chose to not deal with backwards NULL issues for 'Talk.order'
        raise RuntimeError("Cannot reverse this migration. 'Talk.order' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Talk.order'
        db.alter_column('meetups_talk', 'order', self.gf('django.db.models.fields.PositiveSmallIntegerField')())

    models = {
        'meetups.externallink': {
            'Meta': {'object_name': 'ExternalLink'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meetup': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'external_links'", 'to': "orm['meetups.Meetup']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'meetups.meetup': {
            'Meta': {'object_name': 'Meetup', 'ordering': "['-date']"},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_ready': ('django.db.models.fields.BooleanField', [], {}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True'}),
            'sponsors': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'sponsored_meetups'", 'symmetrical': 'False', 'to': "orm['meetups.Sponsor']", 'blank': 'True'}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'meetups'", 'to': "orm['meetups.Venue']", 'blank': 'True'})
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
            'meetup': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'talks'", 'to': "orm['meetups.Meetup']"}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'slides_file': ('django.db.models.fields.files.FileField', [], {'max_length': '500', 'blank': 'True'}),
            'slides_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'speakers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'talks'", 'symmetrical': 'False', 'to': "orm['meetups.Speaker']"}),
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