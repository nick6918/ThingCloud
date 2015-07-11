# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AccountSystem', '0004_auto_20150704_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='userrelation',
            name='uuid',
            field=models.CharField(max_length=100),
        ),
    ]
