# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-08-27 02:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vm', '0004_auto_20180827_0146'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lun_info',
            name='used_space',
        ),
    ]
