# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Reading'
        db.create_table('stats_reading', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('metric', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stats.Metric'])),
            ('instrument', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stats.Instrument'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('method', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('stroke', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('fill', self.gf('django.db.models.fields.CharField')(default='steelblue', max_length=64, blank=True)),
        ))
        db.send_create_signal('stats', ['Reading'])

        # Deleting field 'Instrument.metric'
        db.delete_column('stats_instrument', 'metric_id')

        # Deleting field 'Instrument.aggregations'
        db.delete_column('stats_instrument', 'aggregations')

        # Deleting field 'Instrument.values'
        db.delete_column('stats_instrument', 'values')

        # Deleting field 'Instrument.annotations'
        db.delete_column('stats_instrument', 'annotations')

        # Adding field 'Instrument.stack'
        db.add_column('stats_instrument', 'stack',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Reading'
        db.delete_table('stats_reading')

        # Adding field 'Instrument.metric'
        db.add_column('stats_instrument', 'metric',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['stats.Metric']),
                      keep_default=False)

        # Adding field 'Instrument.aggregations'
        db.add_column('stats_instrument', 'aggregations',
                      self.gf('django.db.models.fields.TextField')(default='[]'),
                      keep_default=False)

        # Adding field 'Instrument.values'
        db.add_column('stats_instrument', 'values',
                      self.gf('django.db.models.fields.TextField')(default='[]'),
                      keep_default=False)

        # Adding field 'Instrument.annotations'
        db.add_column('stats_instrument', 'annotations',
                      self.gf('django.db.models.fields.TextField')(default='[]'),
                      keep_default=False)

        # Deleting field 'Instrument.stack'
        db.delete_column('stats_instrument', 'stack')


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
            'domain': ('django.db.models.fields.IntegerField', [], {'default': '86400'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'readings': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['stats.Metric']", 'through': "orm['stats.Reading']", 'symmetrical': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'stack': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'units': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'width': ('django.db.models.fields.IntegerField', [], {'default': '180'})
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
        },
        'stats.reading': {
            'Meta': {'object_name': 'Reading'},
            'fill': ('django.db.models.fields.CharField', [], {'default': "'steelblue'", 'max_length': '64', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instrument': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stats.Instrument']"}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'metric': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stats.Metric']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'stroke': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'})
        }
    }

    complete_apps = ['stats']