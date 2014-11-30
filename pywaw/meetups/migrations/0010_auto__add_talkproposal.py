# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TalkProposal'
        db.create_table('meetups_talkproposal', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('talk', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['meetups.Talk'])),
            ('message', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('date_submitted', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('meetups', ['TalkProposal'])


    def backwards(self, orm):
        # Deleting model 'TalkProposal'
        db.delete_table('meetups_talkproposal')


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
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_ready': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True'}),
            'sponsors': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'sponsored_meetups'", 'symmetrical': 'False', 'to': "orm['meetups.Sponsor']"}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'meetups'", 'null': 'True', 'to': "orm['meetups.Venue']"})
        },
        'meetups.speaker': {
            'Meta': {'object_name': 'Speaker', 'ordering': "['first_name', 'last_name']"},
            'biography': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'phone': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'max_length': '100'}),
            'website': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '200'})
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
            'meetup': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'talks'", 'null': 'True', 'to': "orm['meetups.Meetup']"}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'slides_file': ('django.db.models.fields.files.FileField', [], {'blank': 'True', 'max_length': '500'}),
            'slides_url': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '200'}),
            'speakers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'talks'", 'symmetrical': 'False', 'to': "orm['meetups.Speaker']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'video_url': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '200'})
        },
        'meetups.talkproposal': {
            'Meta': {'object_name': 'TalkProposal'},
            'date_submitted': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'talk': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['meetups.Talk']"})
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