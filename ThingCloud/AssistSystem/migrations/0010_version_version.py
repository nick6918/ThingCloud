# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AssistSystem', '0009_version'),
    ]

    operations = [
        migrations.AddField(
            model_name='version',
            name='version',
            field=models.CharField(default='0.1.1', max_length=50),
            preserve_default=False,
        ),
    ]
