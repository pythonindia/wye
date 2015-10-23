# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('regions', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(verbose_name='Last Modified At', auto_now=True)),
                ('organisation_type', models.PositiveSmallIntegerField(verbose_name='Organisation Type', choices=[(1, 'College'), (2, 'Free Software Organisation'), (4, 'Others'), (3, 'Student Group')])),
                ('name', models.CharField(max_length=300, unique=True)),
                ('description', models.TextField()),
                ('organisation_role', models.CharField(max_length=300)),
                ('active', models.BooleanField(default=True)),
                ('created_by', models.ForeignKey(related_name='created_organisation_set', blank=True, to=settings.AUTH_USER_MODEL, verbose_name='Created By', null=True)),
                ('location', models.ForeignKey(to='regions.Location')),
                ('modified_by', models.ForeignKey(related_name='updated_organisation_set', blank=True, to=settings.AUTH_USER_MODEL, verbose_name='Modified By', null=True)),
                ('user', models.ManyToManyField(related_name='organisation_users', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'organisations',
            },
        ),
    ]
