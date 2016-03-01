# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AccountSystem', '0010_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='gender',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
