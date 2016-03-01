# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AccountSystem', '0011_address_gender'),
        ('OrderSystem', '0006_auto_20160301_2001'),
    ]

    operations = [
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('cmpid', models.AutoField(serialize=False, primary_key=True)),
                ('state', models.IntegerField()),
                ('notes', models.CharField(max_length=300)),
                ('order', models.ForeignKey(to='OrderSystem.Order')),
                ('user', models.ForeignKey(to='AccountSystem.User')),
            ],
            options={
                'db_table': 'Complaints',
            },
        ),
    ]
