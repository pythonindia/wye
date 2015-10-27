# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0002_auto_20151024_1441'),
    ]

    operations = [
        migrations.AddField(
            model_name='workshopvoting',
            name='rating',
            field=models.ForeignKey(related_name='workshop_rating', default='', to='workshops.WorkshopRatingValues'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='workshopvoting',
            name='presenter_rating',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='workshopvoting',
            name='requester_rating',
            field=models.IntegerField(),
        ),
    ]
