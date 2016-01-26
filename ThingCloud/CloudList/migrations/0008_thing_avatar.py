# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CloudList', '0007_warehouse_typeid'),
    ]

    operations = [
        migrations.AddField(
            model_name='thing',
            name='avatar',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
