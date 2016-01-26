# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CloudList', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='thing',
            old_name='user_belong_to',
            new_name='user_belong_to_id',
        ),
    ]
