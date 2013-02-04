# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Project'
        db.create_table('stats_project', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('stats', ['Project'])

        # Adding model 'Traceback'
        db.create_table('stats_traceback', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stats.Project'])),
            ('trace', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal('stats', ['Traceback'])

        # Deleting field 'ExceptionLog.traceback'
        db.delete_column('stats_exceptionlog', 'traceback')

        # Adding field 'ExceptionLog.project'
        db.add_column('stats_exceptionlog', 'project',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['stats.Project']),
                      keep_default=False)

        # Adding field 'Request.project'
        db.add_column('stats_request', 'project',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['stats.Project']),
                      keep_default=False)

        # Adding field 'Request.traceback'
        db.add_column('stats_request', 'traceback',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stats.Traceback'], null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Project'
        db.delete_table('stats_project')

        # Deleting model 'Traceback'
        db.delete_table('stats_traceback')

        # Adding field 'ExceptionLog.traceback'
        db.add_column('stats_exceptionlog', 'traceback',
                      self.gf('django.db.models.fields.TextField')(null=True),
                      keep_default=False)

        # Deleting field 'ExceptionLog.project'
        db.delete_column('stats_exceptionlog', 'project_id')

        # Deleting field 'Request.project'
        db.delete_column('stats_request', 'project_id')

        # Deleting field 'Request.traceback'
        db.delete_column('stats_request', 'traceback_id')


    models = {
        'stats.exceptionlog': {
            'Meta': {'object_name': 'ExceptionLog'},
            'exception_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'exception_value': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stats.Project']"})
        },
        'stats.project': {
            'Meta': {'object_name': 'Project'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'stats.request': {
            'Meta': {'object_name': 'Request'},
            'exception_log': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stats.ExceptionLog']", 'null': 'True'}),
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
            'trace': ('django.db.models.fields.TextField', [], {'null': 'True'})
        }
    }

    complete_apps = ['stats']