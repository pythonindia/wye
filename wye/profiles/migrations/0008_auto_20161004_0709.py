# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0007_auto_20161003_2241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='interested_level',
            field=models.PositiveSmallIntegerField(blank=True, null=True, choices=[(1, 'Beginner'), (2, 'Intermediate')], verbose_name='Interested Workshop Level'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='no_workshop',
            field=models.IntegerField(default=0, verbose_name='Workshop conducted(apart from pythonexpress)'),
        ),
    ]
