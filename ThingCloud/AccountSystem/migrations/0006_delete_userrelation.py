# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AccountSystem', '0005_auto_20150711_1317'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserRelation',
        ),
    ]
