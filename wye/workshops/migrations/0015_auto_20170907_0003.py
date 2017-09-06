# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0014_workshop_target_audience'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workshop',
            name='target_audience',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Audience', choices=[(1, 'Engineering 4th Year'), (4, 'Engineering 1st Year'), (3, 'Engineering 2ndYear'), (2, 'Engineering 3rd Year'), (10, 'Diploma 1st Year'), (9, 'Diploma 2nd Year'), (8, 'Diploma 3rd Year'), (5, 'MCA Final Year'), (7, 'MCA First Year'), (6, 'MCA Second Year'), (14, 'Others'), (13, 'School'), (12, '10+1'), (11, '10+2')]),
        ),
    ]
