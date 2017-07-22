# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0012_auto_20170212_1701'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workshop',
            name='location',
        ),
        migrations.AddField(
            model_name='workshop',
            name='budget',
            field=models.CharField(null=True, max_length=5),
        ),
        migrations.AddField(
            model_name='workshop',
            name='comments',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='workshop',
            name='hotel_reimbursement',
            field=models.PositiveSmallIntegerField(default=2, verbose_name='Stay Reimbursement Support', choices=[(2, 'No'), (1, 'Yes')]),
        ),
        migrations.AddField(
            model_name='workshop',
            name='reimbursement_mode',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='workshop',
            name='travel_reimbursement',
            field=models.PositiveSmallIntegerField(default=2, verbose_name='Travel Reimbursement Support', choices=[(2, 'No'), (1, 'Yes')]),
        ),
        migrations.AddField(
            model_name='workshop',
            name='tutor_reimbursement_flag',
            field=models.PositiveSmallIntegerField(default=2, verbose_name=' Do you need Travel/Stay reimbursement ?', choices=[(2, 'No'), (1, 'Yes')]),
        ),
    ]
