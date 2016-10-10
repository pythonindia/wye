# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regions', '0001_initial'),
        ('profiles', '0005_auto_20160716_1939'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='enable_notifications',
            field=models.BooleanField(default=True, verbose_name='Email Notification'),
        ),
        migrations.AddField(
            model_name='profile',
            name='interested_states',
            field=models.ManyToManyField(verbose_name='Interested State', null=True, to='regions.State', blank=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='no_workshop',
            field=models.IntegerField(default=0, verbose_name='No. of Workshop conducted'),
        ),
        migrations.AddField(
            model_name='profile',
            name='work_experience',
            field=models.FloatField(verbose_name='Work Experience', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='work_location',
            field=models.TextField(verbose_name='Present Company', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='interested_locations',
            field=models.ManyToManyField(null=True, to='regions.Location', blank=True),
        ),
    ]
