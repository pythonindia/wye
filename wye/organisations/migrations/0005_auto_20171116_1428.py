# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('organisations', '0004_organisation_students'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisation',
            name='students',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='organisation_students', blank=True),
        ),
    ]
