# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('oid', models.IntegerField(serialize=False, primary_key=True)),
                ('phone', models.CharField(max_length=50)),
                ('gender', models.IntegerField(max_length=50)),
                ('name', models.CharField(max_length=100)),
                ('notes', models.CharField(max_length=300)),
                ('fee', models.IntegerField()),
                ('typeid', models.IntegerField()),
                ('itemList', models.CharField(max_length=200)),
                ('state', models.IntegerField()),
                ('pay_state', models.IntegerField()),
                ('create_time', models.DateTimeField()),
                ('paid_time', models.DateTimeField()),
                ('finish_time', models.DateTimeField()),
            ],
            options={
                'db_table': 'orders',
            },
        ),
    ]
