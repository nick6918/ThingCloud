# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('OrderSystem', '0009_viporder'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='showid',
            field=models.CharField(default='201503250001', max_length=50),
            preserve_default=False,
        ),
    ]
