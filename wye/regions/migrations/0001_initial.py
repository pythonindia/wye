# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(verbose_name='Last Modified At', auto_now=True)),
                ('name', models.CharField(max_length=300, unique=True)),
            ],
            options={
                'db_table': 'locations',
            },
        ),
        migrations.CreateModel(
            name='RegionalLead',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('leads', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('location', models.ForeignKey(to='regions.Location')),
            ],
            options={
                'db_table': 'regional_lead',
                'verbose_name': 'RegionalLead',
                'verbose_name_plural': 'RegionalLeads',
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(verbose_name='Last Modified At', auto_now=True)),
                ('name', models.CharField(max_length=300, unique=True)),
            ],
            options={
                'db_table': 'states',
            },
        ),
        migrations.AddField(
            model_name='location',
            name='state',
            field=models.ForeignKey(to='regions.State'),
        ),
    ]
