# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organisations', '0002_auto_20151012_2157'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organisation',
            name='user',
        ),
        migrations.AddField(
            model_name='organisation',
            name='user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='organisation_users'),
        ),
    ]
