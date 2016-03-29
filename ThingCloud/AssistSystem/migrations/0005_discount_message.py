# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AssistSystem', '0004_discount_showcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='discount',
            name='message',
            field=models.CharField(default='test', max_length=300),
            preserve_default=False,
        ),
    ]
