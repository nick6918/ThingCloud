# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AssistSystem', '0007_auto_20160417_1611'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='bannerurl',
            field=models.CharField(default='', max_length=150),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='activity',
            name='url',
            field=models.CharField(default='', max_length=150),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='activity',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='activity',
            name='remark',
            field=models.CharField(max_length=200),
        ),
    ]
