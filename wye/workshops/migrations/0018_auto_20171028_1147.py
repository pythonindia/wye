# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('workshops', '0017_historicalworkshop_historicalworkshop_presenter'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalworkshop',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalworkshop',
            name='requester',
        ),
        migrations.RemoveField(
            model_name='historicalworkshop',
            name='workshop_section',
        ),
        migrations.RemoveField(
            model_name='historicalworkshop_presenter',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalworkshop_presenter',
            name='user',
        ),
        migrations.RemoveField(
            model_name='historicalworkshop_presenter',
            name='workshop',
        ),
        migrations.AddField(
            model_name='workshop',
            name='student_attended',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='workshop_attended'),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='no_of_participants',
            field=models.PositiveIntegerField(choices=[(10, 10), (20, 20), (30, 30), (40, 40), (50, 50), (60, 60)]),
        ),
        migrations.DeleteModel(
            name='HistoricalWorkshop',
        ),
        migrations.DeleteModel(
            name='HistoricalWorkshop_presenter',
        ),
    ]
