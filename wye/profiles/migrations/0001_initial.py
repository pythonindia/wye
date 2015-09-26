# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0001_initial'),
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(related_name='profile', primary_key=True, to=settings.AUTH_USER_MODEL, serialize=False)),
                ('mobile', models.CharField(max_length=10)),
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
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('slug', models.CharField(max_length=100, verbose_name='slug')),
                ('display_name', models.CharField(max_length=300, verbose_name='Display Name')),
                ('active', models.BooleanField(default=1)),
            ],
            options={
                'db_table': 'users_type',
                'verbose_name': 'UserType',
                'ordering': ('-id',),
                'verbose_name_plural': 'UserTypes',
            },
        ),
        migrations.AddField(
            model_name='profile',
            name='usertype',
            field=models.ForeignKey(to='profiles.UserType'),
        ),
    ]
