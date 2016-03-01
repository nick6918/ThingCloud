# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('OrderSystem', '0003_auto_20160301_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='oid',
            field=models.AutoField(serialize=False, primary_key=True),
        ),
    ]
