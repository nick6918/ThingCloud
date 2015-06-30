# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AccountSystem', '0001_AccountSystem_Model_StartUp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='uid',
            field=models.AutoField(serialize=False, primary_key=True),
        ),
    ]
