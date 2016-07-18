# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_auto_20151101_1553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='is_email_visible',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='profile',
            name='is_mobile_visible',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='profile',
            name='usertype',
            field=models.ManyToManyField(null=True, to='profiles.UserType'),
        ),
    ]
