# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AccountSystem', '0015_auto_20160324_1544'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('ctid', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'meta_city',
            },
        ),
        migrations.CreateModel(
            name='Community',
            fields=[
                ('cmid', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('state', models.IntegerField()),
            ],
            options={
                'db_table': 'meta_communities',
            },
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('dsid', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('city_belong', models.ForeignKey(to='AccountSystem.City')),
            ],
            options={
                'db_table': 'meta_districts',
            },
        ),
        migrations.AddField(
            model_name='address',
            name='state',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='community',
            name='district_belong',
            field=models.ForeignKey(to='AccountSystem.District'),
        ),
    ]
