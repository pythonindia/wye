# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0007_auto_20151028_0048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workshop',
            name='no_of_participants',
            field=models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(1000)]),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(3, 'Workshop Accepted '), (5, 'Workshop Completed'), (4, 'Workshop Declined'), (1, 'Draft'), (5, 'FeedBack Pending'), (6, 'Workshop On Hold'), (2, 'Workshop Requested')], verbose_name='Current Status', default=2),
        ),
    ]
