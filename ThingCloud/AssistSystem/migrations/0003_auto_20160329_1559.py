# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AssistSystem', '0002_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='code',
            field=models.CharField(max_length=50),
        ),
    ]
