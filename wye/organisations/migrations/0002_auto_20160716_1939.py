# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisation',
            name='organisation_role',
            field=models.CharField(verbose_name='Your position in organisation', max_length=300),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='organisation_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'College'), (2, 'Free Software Organisation'), (4, 'Others'), (3, 'Student Group')], verbose_name='organisation type'),
        ),
    ]
