# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_auto_20161002_0952'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='interested_level',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Interested Workshop Level', choices=[(1, 'Beginner'), (2, 'Intermediate')]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='profile',
            name='interested_states',
            field=models.ManyToManyField(verbose_name='Interested State *', to='regions.State', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='no_workshop',
            field=models.IntegerField(default=0, verbose_name='No. of Workshop conducted(apart from pythonexpress)'),
        ),
    ]
