# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organisations', '0003_auto_20160815_0955'),
    ]

    operations = [
        migrations.AddField(
            model_name='organisation',
            name='students',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='organisation_students'),
        ),
    ]
