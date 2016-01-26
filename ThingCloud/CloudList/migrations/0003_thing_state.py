# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CloudList', '0002_auto_20160124_1251'),
    ]

    operations = [
        migrations.AddField(
            model_name='thing',
            name='state',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
