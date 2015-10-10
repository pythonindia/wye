# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisations', '0001_initial'),
        ('profiles', '0002_profile_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='interested_locations',
            field=models.ManyToManyField(to='organisations.Location'),
        ),
    ]
