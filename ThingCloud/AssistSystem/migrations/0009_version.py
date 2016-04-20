# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AssistSystem', '0008_auto_20160417_1617'),
    ]

    operations = [
        migrations.CreateModel(
            name='Version',
            fields=[
                ('vrid', models.AutoField(serialize=False, primary_key=True)),
                ('state', models.IntegerField()),
                ('typeid', models.IntegerField()),
                ('compulsorylist', models.CharField(max_length=300)),
                ('selectlist', models.CharField(max_length=300)),
                ('compulsorynotes', models.CharField(max_length=300)),
                ('notes', models.CharField(max_length=300)),
                ('devnotes', models.CharField(max_length=300)),
            ],
            options={
                'db_table': 'meta_version',
            },
        ),
    ]
