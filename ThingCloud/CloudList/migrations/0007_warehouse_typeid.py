# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CloudList', '0006_warehouse_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='warehouse',
            name='typeid',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
