# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ExceptionLog'
        db.create_table('stats_exceptionlog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('exception_type', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('exception_value', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('traceback', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal('stats', ['ExceptionLog'])

        # Adding field 'Request.exception_log'
        db.add_column('stats_request', 'exception_log',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stats.ExceptionLog'], null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'ExceptionLog'
        db.delete_table('stats_exceptionlog')

        # Deleting field 'Request.exception_log'
        db.delete_column('stats_request', 'exception_log_id')


    models = {
        'stats.exceptionlog': {
            'Meta': {'object_name': 'ExceptionLog'},
            'exception_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'exception_value': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'traceback': ('django.db.models.fields.TextField', [], {'null': 'True'})
        },
        'stats.request': {
            'Meta': {'object_name': 'Request'},
            'exception_log': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stats.ExceptionLog']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'time': ('django.db.models.fields.FloatField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['stats']