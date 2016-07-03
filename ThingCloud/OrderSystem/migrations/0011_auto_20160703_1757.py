# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('OrderSystem', '0010_order_showid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='fee',
            field=models.FloatField(),
        ),
    ]
