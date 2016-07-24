# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-24 08:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('OrderSystem', '0004_courier'),
        ('WorkerSystem', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='courier',
            name='worker',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='WorkerSystem.Worker'),
        ),
        migrations.AddField(
            model_name='order',
            name='courier',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='OrderSystem.Courier'),
            preserve_default=False,
        ),
    ]