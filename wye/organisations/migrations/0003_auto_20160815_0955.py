# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisations', '0002_auto_20160716_1939'),
    ]

    operations = [
        migrations.AddField(
            model_name='organisation',
            name='address_map_url',
            field=models.URLField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='organisation',
            name='full_address',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='organisation',
            name='pincode',
            field=models.CharField(max_length=6, null=True, blank=True),
        ),
    ]
