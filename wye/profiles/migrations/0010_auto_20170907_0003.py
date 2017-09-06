# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0009_auto_20170722_2205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='interested_locations',
            field=models.ManyToManyField(to='regions.Location'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='interested_states',
            field=models.ManyToManyField(to='regions.State', verbose_name='Interested State *'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='usertype',
            field=models.ManyToManyField(to='profiles.UserType'),
        ),
    ]
