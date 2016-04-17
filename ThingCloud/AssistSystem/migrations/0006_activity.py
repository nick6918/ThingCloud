# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AssistSystem', '0005_discount_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='activity',
            fields=[
                ('acid', models.AutoField(serialize=False, primary_key=True)),
                ('state', models.IntegerField()),
                ('startdate', models.DateTimeField()),
                ('enddate', models.DateTimeField()),
                ('priority', models.IntegerField()),
                ('name', models.CharField(max_length=300)),
                ('remark', models.CharField(max_length=300)),
                ('discount', models.ForeignKey(to='AssistSystem.Discount')),
            ],
            options={
                'db_table': 'activity',
            },
        ),
    ]
