# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AccountSystem', '0016_auto_20160709_1320'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='community_belong',
            field=models.ForeignKey(default=1, to='AccountSystem.Community'),
            preserve_default=False,
        ),
    ]
