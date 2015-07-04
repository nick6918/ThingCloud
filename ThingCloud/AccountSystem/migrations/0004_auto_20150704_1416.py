# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AccountSystem', '0003_auto_20150630_2011'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSession',
            fields=[
                ('uid', models.IntegerField(serialize=False, primary_key=True)),
                ('session_password', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'user_session',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(default=b'WEIRDUSER', max_length=100),
        ),
    ]
