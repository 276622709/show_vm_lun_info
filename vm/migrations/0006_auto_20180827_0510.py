# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-08-27 05:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vm', '0005_remove_lun_info_used_space'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lun_info',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]