# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0004_auto_20151012_2157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workshop',
            name='no_of_participants',
            field=models.PositiveIntegerField(),
        ),
    ]
