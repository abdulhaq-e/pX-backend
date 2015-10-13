# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UIS', '0007_auto_20150909_0151'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentallowedenrolments',
            name='period_course',
        ),
        migrations.RemoveField(
            model_name='studentallowedenrolments',
            name='student',
        ),
        migrations.DeleteModel(
            name='StudentAllowedEnrolments',
        ),
    ]
