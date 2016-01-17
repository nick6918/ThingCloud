# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AccountSystem', '0006_delete_userrelation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gid',
            field=models.IntegerField(),
        ),
    ]
