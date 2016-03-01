# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AccountSystem', '0010_address'),
        ('OrderSystem', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='addr',
            field=models.ForeignKey(default='', to='AccountSystem.Address'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='gender',
            field=models.IntegerField(),
        ),
    ]
