# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AccountSystem', '0007_auto_20151222_1423'),
    ]

    operations = [
        migrations.CreateModel(
            name='Code',
            fields=[
                ('phone', models.IntegerField(serialize=False, primary_key=True)),
                ('code', models.IntegerField()),
            ],
            options={
                'db_table': 'code_by_phone',
            },
        ),
    ]
