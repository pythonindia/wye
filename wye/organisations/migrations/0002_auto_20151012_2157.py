# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organisations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='organisation',
            name='user',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='organisation',
            name='organisation_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'College'), (2, 'Free Software Organisation'), (4, 'Others'), (3, 'Student Group')], verbose_name='Organisation Type'),
        ),
        migrations.DeleteModel(
            name='OrganisationType',
        ),
    ]
