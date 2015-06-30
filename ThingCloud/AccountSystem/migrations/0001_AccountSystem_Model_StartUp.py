# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('uid', models.IntegerField(serialize=False, primary_key=True)),
                ('gid', models.IntegerField(max_length=10)),
                ('nickname', models.CharField(max_length=200)),
                ('gender', models.CharField(max_length=10, choices=[(b'1', b'MALE'), (b'2', b'FEMAIL')])),
                ('birthday', models.CharField(max_length=50)),
                ('register', models.DateTimeField()),
                ('lastLogin', models.DateTimeField()),
                ('loginIp', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=200)),
                ('salt', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.CreateModel(
            name='UserRelation',
            fields=[
                ('urid', models.IntegerField(serialize=False, primary_key=True)),
                ('uid', models.IntegerField(max_length=10)),
                ('uuid', models.IntegerField(max_length=10)),
            ],
            options={
                'db_table': 'user_relation',
            },
        ),
    ]
