# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0002_auto_20160118_1909'),
    ]

    operations = [
        migrations.CreateModel(
            name='DuplicateUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.IntegerField(default=0, verbose_name='stav', choices=[(0, 'Nevyrie\u0161en\xe9'), (1, 'Nie je duplik\xe1t'), (2, 'Vyrie\u0161en\xfd duplik\xe1t')])),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'duplicitn\xfd pou\u017e\xedvate\u013e',
                'verbose_name_plural': 'duplicitn\xed pou\u017e\xedvatelia',
            },
        ),
    ]
