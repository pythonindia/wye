# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organisations', '0004_organisation_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='organisation',
            name='created_by',
            field=models.ForeignKey(verbose_name='Created By', to=settings.AUTH_USER_MODEL, related_name='created_organisation_set', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='organisation',
            name='modified_by',
            field=models.ForeignKey(verbose_name='Modified By', to=settings.AUTH_USER_MODEL, related_name='updated_organisation_set', blank=True, null=True),
        ),
    ]
