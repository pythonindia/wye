# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_profile_interested_locations'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='usertype',
        ),
        migrations.AddField(
            model_name='profile',
            name='usertype',
            field=models.ManyToManyField(to='profiles.UserType'),
        ),
    ]
