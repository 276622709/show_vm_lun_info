# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-08-27 08:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vm', '0007_auto_20180827_0619'),
    ]

    operations = [
        migrations.AddField(
            model_name='vm_info',
            name='date',
            field=models.DateTimeField(default='2000-07-08 10:00:00'),
        ),
    ]
