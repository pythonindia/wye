# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('regions', '0001_initial'),
        ('organisations', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Workshop',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(verbose_name='Last Modified At', auto_now=True)),
                ('no_of_participants', models.PositiveIntegerField()),
                ('expected_date', models.DateField()),
                ('description', models.TextField()),
                ('workshop_level', models.PositiveSmallIntegerField(verbose_name='Workshop Level', choices=[(1, 'Beginner'), (2, 'Intermediate')])),
                ('is_active', models.BooleanField(default=True)),
                ('status', models.PositiveSmallIntegerField(verbose_name='Current Status', choices=[(3, 'Workshop Accepted '), (5, 'Workshop Completed'), (4, 'Workshop Declined'), (1, 'Draft'), (6, 'Workshop On Hold'), (2, 'Workshop Requested')])),
                ('location', models.ForeignKey(related_name='workshop_location', to='regions.Location')),
                ('presenter', models.ManyToManyField(related_name='workshop_presenter', to=settings.AUTH_USER_MODEL)),
                ('requester', models.ForeignKey(related_name='workshop_requester', to='organisations.Organisation')),
            ],
            options={
                'db_table': 'workshops',
            },
        ),
        migrations.CreateModel(
            name='WorkshopFeedBack',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(verbose_name='Last Modified At', auto_now=True)),
                ('requester_comment', models.TextField()),
                ('presenter_comment', models.TextField()),
                ('workshop', models.ForeignKey(to='workshops.Workshop')),
            ],
            options={
                'db_table': 'workshop_feedback',
            },
        ),
        migrations.CreateModel(
            name='WorkshopRatingValues',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(verbose_name='Last Modified At', auto_now=True)),
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
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(verbose_name='Last Modified At', auto_now=True)),
                ('name', models.CharField(max_length=300, unique=True)),
            ],
            options={
                'db_table': 'workshop_section',
            },
        ),
        migrations.CreateModel(
            name='WorkshopVoting',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(verbose_name='Last Modified At', auto_now=True)),
                ('presenter_rating', models.ForeignKey(related_name='presenter_rating', to='workshops.WorkshopRatingValues')),
                ('requester_rating', models.ForeignKey(related_name='requester_rating', to='workshops.WorkshopRatingValues')),
                ('workshop', models.ForeignKey(to='workshops.Workshop')),
            ],
            options={
                'db_table': 'workshop_votes',
            },
        ),
        migrations.AddField(
            model_name='workshop',
            name='workshop_section',
            field=models.ForeignKey(to='workshops.WorkshopSections'),
        ),
    ]
