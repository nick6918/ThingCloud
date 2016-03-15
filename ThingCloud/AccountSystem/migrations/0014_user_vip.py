# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('VIPSystem', '0002_remove_vip_uid'),
        ('AccountSystem', '0013_remove_user_vip'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='vip',
            field=models.ForeignKey(default=None, to='VIPSystem.VIP'),
            preserve_default=False,
        ),
    ]
