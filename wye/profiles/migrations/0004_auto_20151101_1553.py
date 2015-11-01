# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_auto_20151030_2048'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_email_visible',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='is_mobile_visible',
            field=models.BooleanField(default=True),
        ),
    ]
