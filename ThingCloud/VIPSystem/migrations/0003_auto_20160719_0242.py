# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-18 18:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('VIPSystem', '0002_remove_vip_uid'),
    ]

    operations = [
        migrations.CreateModel(
            name='VIPPackage',
            fields=[
                ('vpid', models.AutoField(primary_key=True, serialize=False)),
                ('start_date', models.DateTimeField()),
                ('days', models.IntegerField()),
                ('level', models.IntegerField()),
                ('nextPackage', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='VIPSystem.VIPPackage')),
            ],
            options={
                'db_table': 'package_vip',
            },
        ),
        migrations.RemoveField(
            model_name='vip',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='vip',
            name='level',
        ),
        migrations.RemoveField(
            model_name='vip',
            name='start_date',
        ),
        migrations.AddField(
            model_name='vip',
            name='currentPackage',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='VIPSystem.VIPPackage'),
        ),
    ]