# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-23 17:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VIP',
            fields=[
                ('vid', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'user_vip',
            },
        ),
        migrations.CreateModel(
            name='VIPPackage',
            fields=[
                ('vpid', models.AutoField(primary_key=True, serialize=False)),
                ('start_date', models.DateTimeField(default=None, null=True)),
                ('days', models.IntegerField()),
                ('level', models.IntegerField()),
                ('merged', models.IntegerField(default=0)),
                ('nextPackage', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='VIPSystem.VIPPackage')),
            ],
            options={
                'db_table': 'package_vip',
            },
        ),
        migrations.AddField(
            model_name='vip',
            name='headPackage',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='VIPSystem.VIPPackage'),
        ),
    ]
