# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0006_remove_workshopratingvalues_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workshop',
            name='status',
            field=models.PositiveSmallIntegerField(verbose_name='Current Status', default=1, choices=[(3, 'Workshop Accepted '), (5, 'Workshop Completed'), (4, 'Workshop Declined'), (1, 'Draft'), (5, 'FeedBack Pending'), (6, 'Workshop On Hold'), (2, 'Workshop Requested')]),
        ),
        migrations.AlterField(
            model_name='workshopfeedback',
            name='feedback_type',
            field=models.PositiveSmallIntegerField(verbose_name='User_type', choices=[(2, 'Organisation'), (1, 'Presenter')]),
        ),
    ]
