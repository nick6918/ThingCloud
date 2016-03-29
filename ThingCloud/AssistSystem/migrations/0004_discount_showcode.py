# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AssistSystem', '0003_auto_20160329_1559'),
    ]

    operations = [
        migrations.AddField(
            model_name='discount',
            name='showcode',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
