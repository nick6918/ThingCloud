# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-24 08:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CloudList', '0001_initial'),
        ('OrderSystem', '0003_auto_20160724_0148'),
    ]

    operations = [
        migrations.CreateModel(
            name='Courier',
            fields=[
                ('crid', models.AutoField(primary_key=True, serialize=False)),
                ('wh_belong', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CloudList.WareHouse')),
            ],
            options={
                'db_table': 'work_courier',
            },
        ),
    ]