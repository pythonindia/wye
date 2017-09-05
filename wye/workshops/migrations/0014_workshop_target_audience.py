# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0013_auto_20170617_1409'),
    ]

    operations = [
        migrations.AddField(
            model_name='workshop',
            name='target_audience',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Audience', choices=[(1, 'B.E Final Year'), (4, 'B.E Second Year'), (3, 'B.E Second Year'), (2, 'B.E Third Year'), (5, 'MASTER Final Year'), (7, 'MASTER Second Year'), (6, 'MASTER Second Year'), (11, 'Others'), (10, 'School'), (9, 'College 1 Year'), (8, 'College 2nd year')]),
        ),
    ]
