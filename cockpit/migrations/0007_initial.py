# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PageTranslation'
        db.create_table(u'cockpit_page_translation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('heading', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('content', self.gf('ckeditor.fields.RichTextField')()),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
            ('master', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', null=True, to=orm['cockpit.Page'])),
        ))
        db.send_create_signal(u'cockpit', ['PageTranslation'])

        # Adding unique constraint on 'PageTranslation', fields ['language_code', 'master']
        db.create_unique(u'cockpit_page_translation', ['language_code', 'master_id'])

        # Adding model 'Page'
        db.create_table(u'cockpit_page', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['cockpit.Page'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal(u'cockpit', ['Page'])


    def backwards(self, orm):
        # Removing unique constraint on 'PageTranslation', fields ['language_code', 'master']
        db.delete_unique(u'cockpit_page_translation', ['language_code', 'master_id'])

        # Deleting model 'PageTranslation'
        db.delete_table(u'cockpit_page_translation')

        # Deleting model 'Page'
        db.delete_table(u'cockpit_page')


    models = {
        u'cockpit.page': {
            'Meta': {'object_name': 'Page'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['cockpit.Page']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'cockpit.pagetranslation': {
            'Meta': {'unique_together': "[('language_code', 'master')]", 'object_name': 'PageTranslation', 'db_table': "u'cockpit_page_translation'"},
            'content': ('ckeditor.fields.RichTextField', [], {}),
            'heading': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'null': 'True', 'to': u"orm['cockpit.Page']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        }
    }

    complete_apps = ['cockpit']