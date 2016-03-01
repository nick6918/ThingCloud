# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AccountSystem', '0009_auto_20160126_1617'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('adid', models.AutoField(serialize=False, primary_key=True)),
                ('addr', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=100)),
                ('is_default', models.IntegerField()),
                ('tagid', models.IntegerField()),
                ('user', models.ForeignKey(to='AccountSystem.User')),
            ],
            options={
                'db_table': 'user_address',
            },
        ),
    ]
