# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AccountSystem', '0007_auto_20151222_1423'),
    ]

    operations = [
        migrations.CreateModel(
            name='Thing',
            fields=[
                ('tid', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('notes', models.CharField(max_length=200)),
                ('time_saved', models.DateTimeField()),
                ('typeid', models.IntegerField()),
                ('subtype_name', models.CharField(max_length=100)),
                ('gender', models.IntegerField()),
                ('user_belong_to', models.ForeignKey(to='AccountSystem.User')),
            ],
            options={
                'db_table': 'things',
            },
        ),
        migrations.CreateModel(
            name='WareHouse',
            fields=[
                ('wid', models.AutoField(serialize=False, primary_key=True)),
                ('addr', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='thing',
            name='wh_in',
            field=models.ForeignKey(to='CloudList.WareHouse'),
        ),
    ]
