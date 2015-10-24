# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workshop',
            name='status',
            field=models.PositiveSmallIntegerField(default=1, verbose_name=b'Current Status', choices=[(3, 'Workshop Accepted '), (5, 'Workshop Completed'), (4, 'Workshop Declined'), (1, 'Draft'), (6, 'Workshop On Hold'), (2, 'Workshop Requested')]),
        ),
    ]
