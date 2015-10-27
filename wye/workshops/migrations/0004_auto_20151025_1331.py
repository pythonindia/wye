# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0003_auto_20151025_0818'),
    ]

    operations = [
        migrations.RenameField(
            model_name='workshopfeedback',
            old_name='presenter_comment',
            new_name='comment',
        ),
        migrations.RemoveField(
            model_name='workshopfeedback',
            name='requester_comment',
        ),
        migrations.RemoveField(
            model_name='workshopvoting',
            name='presenter_rating',
        ),
        migrations.RemoveField(
            model_name='workshopvoting',
            name='requester_rating',
        ),
        migrations.RemoveField(
            model_name='workshopvoting',
            name='workshop',
        ),
        migrations.AddField(
            model_name='workshopfeedback',
            name='user_type',
            field=models.PositiveSmallIntegerField(default=0, verbose_name=b'User_type', choices=[(2, 'Organisation'), (1, 'Presenter')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='workshopvoting',
            name='workshop_feedback',
            field=models.ForeignKey(related_name='workshop_feedback', default='', to='workshops.WorkshopFeedBack'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='workshopvoting',
            name='workshop_rating',
            field=models.ForeignKey(related_name='workshop_rating', default='', to='workshops.WorkshopRatingValues'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='workshopvoting',
            name='rating',
            field=models.IntegerField(),
        ),
    ]
