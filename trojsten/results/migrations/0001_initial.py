# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FrozenResults'
        db.create_table(u'results_frozenresults', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('round', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contests.Round'])),
            ('is_single_round', self.gf('django.db.models.fields.BooleanField')()),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tasks.Category'])),
        ))
        db.send_create_signal(u'results', ['FrozenResults'])

        # Adding model 'FrozenPoints'
        db.create_table(u'results_frozenpoints', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tasks.Task'])),
            ('description_points', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('source_points', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
        ))
        db.send_create_signal(u'results', ['FrozenPoints'])

        # Adding model 'FrozenUserResult'
        db.create_table(u'results_frozenuserresult', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('frozenresults', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['results.FrozenResults'])),
            ('original_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.User'])),
            ('rank', self.gf('django.db.models.fields.IntegerField')()),
            ('fullname', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('school_year', self.gf('django.db.models.fields.IntegerField')()),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.School'])),
            ('previous_points', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('sum', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
        ))
        db.send_create_signal(u'results', ['FrozenUserResult'])

        # Adding M2M table for field task_points on 'FrozenUserResult'
        m2m_table_name = db.shorten_name(u'results_frozenuserresult_task_points')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('frozenuserresult', models.ForeignKey(orm[u'results.frozenuserresult'], null=False)),
            ('frozenpoints', models.ForeignKey(orm[u'results.frozenpoints'], null=False))
        ))
        db.create_unique(m2m_table_name, ['frozenuserresult_id', 'frozenpoints_id'])


    def backwards(self, orm):
        # Deleting model 'FrozenResults'
        db.delete_table(u'results_frozenresults')

        # Deleting model 'FrozenPoints'
        db.delete_table(u'results_frozenpoints')

        # Deleting model 'FrozenUserResult'
        db.delete_table(u'results_frozenuserresult')

        # Removing M2M table for field task_points on 'FrozenUserResult'
        db.delete_table(db.shorten_name(u'results_frozenuserresult_task_points'))


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'contests.competition': {
            'Meta': {'object_name': 'Competition'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'organizers_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.Group']", 'null': 'True'}),
            'repo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contests.Repository']", 'null': 'True', 'blank': 'True'}),
            'repo_root': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['sites.Site']", 'symmetrical': 'False'})
        },
        u'contests.repository': {
            'Meta': {'object_name': 'Repository'},
            'notification_string': ('uuidfield.fields.UUIDField', [], {'unique': 'True', 'max_length': '32', 'primary_key': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'contests.round': {
            'Meta': {'object_name': 'Round'},
            'end_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 11, 22, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'series': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contests.Series']"}),
            'solutions_visible': ('django.db.models.fields.BooleanField', [], {}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 11, 22, 0, 0)'}),
            'visible': ('django.db.models.fields.BooleanField', [], {})
        },
        u'contests.series': {
            'Meta': {'object_name': 'Series'},
            'competition': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contests.Competition']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        },
        u'people.address': {
            'Meta': {'object_name': 'Address'},
            'country': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '16', 'db_index': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'town': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'})
        },
        u'people.school': {
            'Meta': {'ordering': "(u'city', u'street', u'verbose_name')", 'object_name': 'School'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'addr_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'verbose_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'})
        },
        u'people.user': {
            'Meta': {'object_name': 'User'},
            'birth_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_index': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "u'M'", 'max_length': '1'}),
            'graduation': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            'home_address': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'lives_here'", 'null': 'True', 'to': u"orm['people.Address']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'mailing_address': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'accepting_mails_here'", 'null': 'True', 'to': u"orm['people.Address']"}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['people.School']", 'null': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'results.frozenpoints': {
            'Meta': {'object_name': 'FrozenPoints'},
            'description_points': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source_points': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tasks.Task']"})
        },
        u'results.frozenresults': {
            'Meta': {'object_name': 'FrozenResults'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tasks.Category']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_single_round': ('django.db.models.fields.BooleanField', [], {}),
            'round': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contests.Round']"})
        },
        u'results.frozenuserresult': {
            'Meta': {'object_name': 'FrozenUserResult'},
            'frozenresults': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['results.FrozenResults']"}),
            'fullname': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['people.User']"}),
            'previous_points': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'rank': ('django.db.models.fields.IntegerField', [], {}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['people.School']"}),
            'school_year': ('django.db.models.fields.IntegerField', [], {}),
            'sum': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'task_points': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['results.FrozenPoints']", 'symmetrical': 'False'})
        },
        u'sites.site': {
            'Meta': {'ordering': "(u'domain',)", 'object_name': 'Site', 'db_table': "u'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'tasks.category': {
            'Meta': {'object_name': 'Category'},
            'competition': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contests.Competition']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        u'tasks.task': {
            'Meta': {'object_name': 'Task'},
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['tasks.Category']", 'symmetrical': 'False', 'blank': 'True'}),
            'description_points': ('django.db.models.fields.IntegerField', [], {}),
            'external_submit_link': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'has_description': ('django.db.models.fields.BooleanField', [], {}),
            'has_source': ('django.db.models.fields.BooleanField', [], {}),
            'has_testablezip': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'integer_source_points': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'reviewer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['people.User']", 'null': 'True', 'blank': 'True'}),
            'round': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contests.Round']"}),
            'source_points': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['results']