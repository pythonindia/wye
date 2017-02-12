# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0011_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='workshopratingvalues',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='workshopsections',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='status',
            field=models.PositiveSmallIntegerField(verbose_name='Current Status', choices=[(3, 'Workshop Accepted '), (7, 'Workshop Completed'), (4, 'Workshop Declined'), (1, 'Draft'), (5, 'FeedBack Pending'), (6, 'Workshop On Hold'), (2, 'Workshop Requested'), (8, 'Workshop unable to complete')], default=2),
        ),
    ]
