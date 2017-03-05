# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0009_auto_20161017_0059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workshop',
            name='number_of_volunteers',
            field=models.PositiveSmallIntegerField(default=0, null=True, blank=True),
        ),
    ]
