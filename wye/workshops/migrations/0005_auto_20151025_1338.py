# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0004_auto_20151025_1331'),
    ]

    operations = [
        migrations.RenameField(
            model_name='workshopfeedback',
            old_name='user_type',
            new_name='feedback_type',
        ),
    ]
