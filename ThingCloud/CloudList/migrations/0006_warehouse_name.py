# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CloudList', '0005_auto_20160124_1350'),
    ]

    operations = [
        migrations.AddField(
            model_name='warehouse',
            name='name',
            field=models.CharField(default='hello', max_length=50),
            preserve_default=False,
        ),
    ]
