# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AccountSystem', '0011_address_gender'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('fdid', models.AutoField(serialize=False, primary_key=True)),
                ('notes', models.CharField(max_length=300)),
                ('state', models.IntegerField()),
                ('user', models.ForeignKey(to='AccountSystem.User')),
            ],
            options={
                'db_table': 'feedbacks',
            },
        ),
    ]
