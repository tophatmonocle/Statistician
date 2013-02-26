# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Metric.slug'
        db.add_column('stats_metric', 'slug',
                      self.gf('django.db.models.fields.SlugField')(default='online_students', max_length=50),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Metric.slug'
        db.delete_column('stats_metric', 'slug')


    models = {
        'stats.exceptionlog': {
            'Meta': {'object_name': 'ExceptionLog'},
            'exception_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'exception_value': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stats.Project']"})
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
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        'stats.project': {
            'Meta': {'object_name': 'Project'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'stats.request': {
            'Meta': {'object_name': 'Request'},
            'exception_log': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stats.ExceptionLog']", 'null': 'True'}),
            'hostname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stats.Project']"}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'time': ('django.db.models.fields.FloatField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'traceback': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stats.Traceback']", 'null': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'stats.traceback': {
            'Meta': {'object_name': 'Traceback'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stats.Project']"}),
            'trace': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['stats']