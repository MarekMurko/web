# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-07 12:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('people', '0005_auto_20160607_1400')
    ]

    state_operations = [
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('abbreviation', models.CharField(blank=True, help_text='Sktatka n\xe1zvu \u0161koly.', max_length=100, verbose_name='skratka')),
                ('verbose_name', models.CharField(max_length=100, verbose_name='cel\xfd n\xe1zov')),
                ('addr_name', models.CharField(blank=True, max_length=100, verbose_name='n\xe1zov v adrese')),
                ('street', models.CharField(blank=True, max_length=100, verbose_name='ulica')),
                ('city', models.CharField(blank=True, max_length=100, verbose_name='mesto')),
                ('zip_code', models.CharField(blank=True, max_length=10, verbose_name='PS\u010c')),
            ],
            options={
                'ordering': ('city', 'street', 'verbose_name'),
                'verbose_name': '\u0161kola',
                'verbose_name_plural': '\u0161koly',
            },
        ),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(state_operations=state_operations)
    ]