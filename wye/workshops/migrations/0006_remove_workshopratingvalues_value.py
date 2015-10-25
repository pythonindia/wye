# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0005_auto_20151025_1338'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workshopratingvalues',
            name='value',
        ),
    ]
