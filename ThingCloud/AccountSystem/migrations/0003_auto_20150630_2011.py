# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AccountSystem', '0002_AccountSystem_Auto_Increment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userrelation',
            name='urid',
            field=models.AutoField(serialize=False, primary_key=True),
        ),
    ]
