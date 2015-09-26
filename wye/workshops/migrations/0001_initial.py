# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('organisations', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Workshop',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Last Modified At')),
                ('no_of_participants', models.IntegerField()),
                ('expected_date', models.DateField()),
                ('description', models.TextField()),
                ('location', models.ForeignKey(to='organisations.Location', related_name='workshop_location')),
                ('presenter', models.ManyToManyField(related_name='workshop_presenter', to=settings.AUTH_USER_MODEL)),
                ('requester', models.ForeignKey(to='organisations.Organisation', related_name='workshop_requester')),
            ],
            options={
                'db_table': 'workshops',
            },
        ),
        migrations.CreateModel(
            name='WorkshopFeedBack',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Last Modified At')),
                ('requester_comment', models.TextField()),
                ('presenter_comment', models.TextField()),
                ('workshop', models.ForeignKey(to='workshops.Workshop')),
            ],
            options={
                'db_table': 'workshop_feedback',
            },
        ),
        migrations.CreateModel(
            name='WorkshopLevel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Last Modified At')),
                ('name', models.CharField(max_length=300, unique=True)),
            ],
            options={
                'db_table': 'workshop_level',
            },
        ),
        migrations.CreateModel(
            name='WorkshopRatingValues',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Last Modified At')),
                ('value', models.IntegerField()),
                ('name', models.CharField(max_length=300)),
            ],
            options={
                'db_table': 'workshop_vote_value',
            },
        ),
        migrations.CreateModel(
            name='WorkshopSections',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Last Modified At')),
                ('name', models.CharField(max_length=300, unique=True)),
            ],
            options={
                'db_table': 'workshop_section',
            },
        ),
        migrations.CreateModel(
            name='WorkshopVoting',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Last Modified At')),
                ('presenter_rating', models.ForeignKey(to='workshops.WorkshopRatingValues', related_name='presenter_rating')),
                ('requester_rating', models.ForeignKey(to='workshops.WorkshopRatingValues', related_name='requester_rating')),
                ('workshop', models.ForeignKey(to='workshops.Workshop')),
            ],
            options={
                'db_table': 'workshop_votes',
            },
        ),
        migrations.AddField(
            model_name='workshop',
            name='workshop_level',
            field=models.ForeignKey(to='workshops.WorkshopLevel'),
        ),
        migrations.AddField(
            model_name='workshop',
            name='workshop_section',
            field=models.ForeignKey(to='workshops.WorkshopSections'),
        ),
    ]
