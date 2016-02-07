# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('periods', '0001_initial'),
        ('period_registrations', '0002_periodregistration_section_enrolments'),
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='periods',
            field=models.ManyToManyField(related_name='students', through='period_registrations.PeriodRegistration', to='periods.Period'),
        ),
    ]
