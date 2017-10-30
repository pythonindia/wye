# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organisations', '0003_auto_20160815_0955'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('workshops', '0016_auto_20171013_1506'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalWorkshop',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, blank=True, auto_created=True)),
                ('created_at', models.DateTimeField(verbose_name='Created At', blank=True, editable=False)),
                ('modified_at', models.DateTimeField(verbose_name='Last Modified At', blank=True, editable=False)),
                ('no_of_participants', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(1000)])),
                ('expected_date', models.DateField()),
                ('description', models.TextField()),
                ('workshop_level', models.PositiveSmallIntegerField(verbose_name='Workshop Level', choices=[(2, 'Advance'), (1, 'Beginner'), (2, 'Intermediate')])),
                ('number_of_volunteers', models.PositiveSmallIntegerField(blank=True, default=0, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('status', models.PositiveSmallIntegerField(verbose_name='Current Status', default=2, choices=[(3, 'Workshop Accepted '), (7, 'Workshop Completed'), (4, 'Workshop Declined'), (1, 'Draft'), (5, 'FeedBack Pending'), (6, 'Workshop On Hold'), (2, 'Workshop Requested'), (8, 'Workshop unable to complete')])),
                ('travel_reimbursement', models.PositiveSmallIntegerField(verbose_name='Travel Reimbursement Support', default=2, choices=[(2, 'No'), (1, 'Yes')])),
                ('hotel_reimbursement', models.PositiveSmallIntegerField(verbose_name='Stay Reimbursement Support', default=2, choices=[(2, 'No'), (1, 'Yes')])),
                ('budget', models.CharField(max_length=5, null=True)),
                ('reimbursement_mode', models.TextField(null=True)),
                ('tutor_reimbursement_flag', models.PositiveSmallIntegerField(verbose_name=' Do you need Travel/Stay reimbursement ?', default=2, choices=[(2, 'No'), (1, 'Yes')])),
                ('comments', models.TextField()),
                ('target_audience', models.PositiveSmallIntegerField(verbose_name='Audience', default=1, choices=[(1, 'Engineering 4th Year'), (4, 'Engineering 1st Year'), (3, 'Engineering 2ndYear'), (2, 'Engineering 3rd Year'), (10, 'Diploma 1st Year'), (9, 'Diploma 2nd Year'), (8, 'Diploma 3rd Year'), (5, 'MCA Final Year'), (7, 'MCA First Year'), (6, 'MCA Second Year'), (14, 'Others'), (13, 'School'), (12, '10+1'), (11, '10+2')])),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, null=True, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('requester', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, blank=True, null=True, related_name='+', db_constraint=False, to='organisations.Organisation')),
                ('workshop_section', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, blank=True, null=True, related_name='+', db_constraint=False, to='workshops.WorkshopSections')),
            ],
            options={
                'verbose_name': 'historical workshop',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalWorkshop_presenter',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, blank=True, auto_created=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, null=True, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, blank=True, null=True, related_name='+', db_constraint=False, to=settings.AUTH_USER_MODEL)),
                ('workshop', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, blank=True, null=True, related_name='+', db_constraint=False, to='workshops.Workshop')),
            ],
            options={
                'verbose_name': 'historical workshop-user relationship',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
    ]
