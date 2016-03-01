# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AccountSystem', '0011_address_gender'),
        ('OrderSystem', '0005_order_prepayid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='pay_state',
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(default=4, to='AccountSystem.User'),
            preserve_default=False,
        ),
    ]
