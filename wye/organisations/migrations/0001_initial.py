# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Last Modified At')),
                ('name', models.CharField(max_length=300, unique=True)),
            ],
            options={
                'db_table': 'locations',
            },
        ),
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Last Modified At')),
                ('name', models.CharField(max_length=300, unique=True)),
                ('description', models.TextField()),
                ('organisation_role', models.CharField(max_length=300)),
                ('location', models.ForeignKey(to='organisations.Location')),
            ],
            options={
                'db_table': 'organisations',
            },
        ),
        migrations.CreateModel(
            name='OrganisationType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Last Modified At')),
                ('name', models.CharField(max_length=300, unique=True)),
            ],
            options={
                'db_table': 'organisation_types',
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Last Modified At')),
                ('name', models.CharField(max_length=300, unique=True)),
            ],
            options={
                'db_table': 'states',
            },
        ),
        migrations.AddField(
            model_name='organisation',
            name='organisation_type',
            field=models.ForeignKey(to='organisations.OrganisationType'),
        ),
        migrations.AddField(
            model_name='location',
            name='state',
            field=models.ForeignKey(to='organisations.State'),
        ),
    ]
