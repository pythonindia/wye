# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0010_auto_20170907_0003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='interested_level',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(2, 'Advance'), (1, 'Beginner'), (2, 'Intermediate')], verbose_name='Interested Workshop Level', null=True),
        ),
    ]
