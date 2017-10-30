# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('workshops', '0015_auto_20170907_0003'),
    ]

    operations = [
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
        migrations.AlterField(
            model_name='workshop',
            name='workshop_level',
            field=models.PositiveSmallIntegerField(verbose_name='Workshop Level', choices=[(2, 'Advance'), (1, 'Beginner'), (2, 'Intermediate')]),
        ),
    ]
