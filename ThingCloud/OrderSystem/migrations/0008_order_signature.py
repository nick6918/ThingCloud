# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('OrderSystem', '0007_complaint'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='signature',
            field=models.CharField(default='ABCDEFGH', max_length=50),
            preserve_default=False,
        ),
    ]
