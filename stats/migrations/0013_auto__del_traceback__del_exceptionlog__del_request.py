# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Traceback'
        db.delete_table('stats_traceback')

        # Deleting model 'ExceptionLog'
        db.delete_table('stats_exceptionlog')

        # Deleting model 'Request'
        db.delete_table('stats_request')


    def backwards(self, orm):
        # Adding model 'Traceback'
        db.create_table('stats_traceback', (
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stats.Project'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('trace', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('stats', ['Traceback'])

        # Adding model 'ExceptionLog'
        db.create_table('stats_exceptionlog', (
            ('exception_type', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stats.Project'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('exception_value', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('stats', ['ExceptionLog'])

        # Adding model 'Request'
        db.create_table('stats_request', (
            ('status', self.gf('django.db.models.fields.IntegerField')()),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('traceback', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stats.Traceback'], null=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('exception_log', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stats.ExceptionLog'], null=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('hostname', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stats.Project'])),
            ('time', self.gf('django.db.models.fields.FloatField')()),
            ('method', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('stats', ['Request'])


    models = {
        'stats.event': {
            'Meta': {'object_name': 'Event'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stats.Project']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'stats.instrument': {
            'Meta': {'object_name': 'Instrument'},
            'aggregations': ('django.db.models.fields.TextField', [], {'default': "'[]'"}),
            'annotations': ('django.db.models.fields.TextField', [], {'default': "'[]'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metric': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stats.Metric']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'values': ('django.db.models.fields.TextField', [], {'default': "'[]'"})
        },
        'stats.metric': {
            'Meta': {'object_name': 'Metric'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stats.Project']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'stats.metricdata': {
            'Meta': {'object_name': 'MetricData'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metric': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stats.Metric']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        'stats.project': {
            'Meta': {'object_name': 'Project'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['stats']