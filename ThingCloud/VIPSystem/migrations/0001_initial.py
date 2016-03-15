# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AccountSystem', '0011_address_gender'),
    ]

    operations = [
        migrations.CreateModel(
            name='VIP',
            fields=[
                ('vid', models.AutoField(serialize=False, primary_key=True)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('level', models.IntegerField()),
                ('uid', models.ForeignKey(to='AccountSystem.User')),
            ],
            options={
                'db_table': 'user_vip',
            },
        ),
    ]
