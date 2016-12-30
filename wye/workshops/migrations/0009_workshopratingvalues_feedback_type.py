# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0008_auto_20160716_1939'),
    ]

    operations = [
        migrations.AddField(
            model_name='workshopratingvalues',
            name='feedback_type',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='User_type', choices=[(2, 'Organisation'), (1, 'Presenter')]),
            preserve_default=False,
        ),
    ]
