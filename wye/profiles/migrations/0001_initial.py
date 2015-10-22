# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('regions', '0001_initial'),
        ('workshops', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, related_name='profile')),
                ('slug', models.CharField(max_length=100, unique=True)),
                ('mobile', models.CharField(max_length=10)),
                ('interested_locations', models.ManyToManyField(to='regions.Location')),
                ('interested_sections', models.ManyToManyField(to='workshops.WorkshopSections')),
            ],
            options={
                'db_table': 'user_profile',
                'verbose_name': 'UserProfile',
                'verbose_name_plural': 'UserProfiles',
            },
        ),
        migrations.CreateModel(
            name='UserType',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('slug', models.CharField(max_length=100, verbose_name='slug')),
                ('display_name', models.CharField(max_length=300, verbose_name='Display Name')),
                ('active', models.BooleanField(default=1)),
            ],
            options={
                'db_table': 'users_type',
                'ordering': ('-id',),
                'verbose_name_plural': 'UserTypes',
                'verbose_name': 'UserType',
            },
        ),
        migrations.AddField(
            model_name='profile',
            name='usertype',
            field=models.ManyToManyField(to='profiles.UserType'),
        ),
    ]
