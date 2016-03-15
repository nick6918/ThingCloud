# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AccountSystem', '0012_user_vip'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='vip',
        ),
    ]
