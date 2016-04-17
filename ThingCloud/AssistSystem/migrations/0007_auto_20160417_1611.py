# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AssistSystem', '0006_activity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='enddate',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='startdate',
        ),
    ]
