# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisations', '0003_auto_20151013_1830'),
    ]

    operations = [
        migrations.AddField(
            model_name='organisation',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
