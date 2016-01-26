# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AccountSystem', '0008_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='code',
            name='phone',
            field=models.CharField(max_length=50, serialize=False, primary_key=True),
        ),
    ]
