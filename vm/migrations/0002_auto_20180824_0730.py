# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-08-24 07:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vm', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lun_info',
            name='all_space',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='lun_info',
            name='free_space',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='lun_info',
            name='used_space',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='vm_info',
            name='vm_cpu',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='vm_info',
            name='vm_disk',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='vm_info',
            name='vm_mem',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='vm_info',
            name='vm_used_space',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='vm_used_space_day',
            name='vm_used_space',
            field=models.BigIntegerField(),
        ),
    ]