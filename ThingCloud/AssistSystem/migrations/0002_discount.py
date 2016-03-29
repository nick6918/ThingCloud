# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AccountSystem', '0015_auto_20160324_1544'),
        ('AssistSystem', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('dsid', models.AutoField(serialize=False, primary_key=True)),
                ('detail', models.CharField(max_length=300)),
                ('state', models.IntegerField()),
                ('code', models.ForeignKey(to='AccountSystem.User')),
            ],
            options={
                'db_table': 'discount',
            },
        ),
    ]
