# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regions', '0001_initial'),
        ('profiles', '0002_remove_profile_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='facebook',
            field=models.URLField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='github',
            field=models.URLField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='googleplus',
            field=models.URLField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='linkedin',
            field=models.URLField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='location',
            field=models.ForeignKey(null=True, related_name='user_location', to='regions.Location'),
        ),
        migrations.AddField(
            model_name='profile',
            name='picture',
            field=models.ImageField(default='images/newuser.png', upload_to='images/'),
        ),
        migrations.AddField(
            model_name='profile',
            name='slideshare',
            field=models.URLField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='twitter',
            field=models.URLField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='mobile',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
