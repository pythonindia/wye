# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0015_auto_20170907_0003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workshop',
            name='workshop_level',
            field=models.PositiveSmallIntegerField(choices=[(2, 'Advance'), (1, 'Beginner'), (2, 'Intermediate')], verbose_name='Workshop Level'),
        ),
    ]
