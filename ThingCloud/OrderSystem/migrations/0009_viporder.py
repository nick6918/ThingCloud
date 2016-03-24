# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AccountSystem', '0015_auto_20160324_1544'),
        ('OrderSystem', '0008_order_signature'),
    ]

    operations = [
        migrations.CreateModel(
            name='VIPOrder',
            fields=[
                ('void', models.AutoField(serialize=False, primary_key=True)),
                ('month', models.IntegerField()),
                ('level', models.IntegerField()),
                ('prepayid', models.CharField(max_length=50)),
                ('fee', models.CharField(max_length=50)),
                ('state', models.IntegerField()),
                ('user', models.ForeignKey(to='AccountSystem.User')),
            ],
            options={
                'db_table': 'order_vip',
            },
        ),
    ]
