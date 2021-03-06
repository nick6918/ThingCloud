# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-24 08:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('AccountSystem', '0002_auto_20160724_0126'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('eid', models.AutoField(primary_key=True, serialize=False)),
                ('phone', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='AccountSystem.User')),
            ],
            options={
                'db_table': 'work_employee',
            },
        ),
    ]
