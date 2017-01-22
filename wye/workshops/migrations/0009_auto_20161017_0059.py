# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('workshops', '0008_auto_20160716_1939'),
    ]

    operations = [
        migrations.AddField(
            model_name='workshop',
            name='number_of_volunteers',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='workshop',
            name='volunteer',
            field=models.ManyToManyField(related_name='workshop_volunteer', to=settings.AUTH_USER_MODEL),
        ),
    ]
