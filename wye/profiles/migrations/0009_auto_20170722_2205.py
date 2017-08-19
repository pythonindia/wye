# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0008_auto_20161004_0709'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='occupation',
            field=models.CharField(max_length=300, blank=True, null=True, verbose_name='Occupation'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='work_experience',
            field=models.FloatField(null=True, blank=True, verbose_name='Work Experience(If Any)'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='work_location',
            field=models.CharField(max_length=500, blank=True, null=True, verbose_name='Organisaiton/Company'),
        ),
    ]
