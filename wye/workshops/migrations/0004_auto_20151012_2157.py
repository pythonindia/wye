# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0003_workshop_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workshop',
            name='workshop_level',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Beginner'), (2, 'Intermediate')], verbose_name='Workshop Level'),
        ),
        migrations.DeleteModel(
            name='WorkshopLevel',
        ),
    ]
