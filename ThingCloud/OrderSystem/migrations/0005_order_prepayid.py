# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('OrderSystem', '0004_auto_20160301_1435'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='prepayid',
            field=models.CharField(default=10001, max_length=50),
            preserve_default=False,
        ),
    ]
