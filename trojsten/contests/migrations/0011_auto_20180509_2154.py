# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-05-09 21:54
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contests', '0010_round_results_final'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='taskpeople',
            options={'verbose_name': 'Assigned user', 'verbose_name_plural': 'Assigned people'},
        ),
        migrations.AddField(
            model_name='task',
            name='email_on_code_submit',
            field=models.BooleanField(default=False, verbose_name='Zaslať notifikáciu o submite kódu opravovateľom'),
        ),
        migrations.AddField(
            model_name='task',
            name='email_on_desc_submit',
            field=models.BooleanField(default=False, verbose_name='Zaslať notifikáciu o submite popisu opravovateľom'),
        ),
        migrations.AlterField(
            model_name='taskpeople',
            name='role',
            field=models.IntegerField(choices=[(0, 'reviewer'), (1, 'solution writer'), (2, 'proofreader')], verbose_name='role'),
        ),
        migrations.AlterField(
            model_name='taskpeople',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='organizer'),
        ),
    ]
