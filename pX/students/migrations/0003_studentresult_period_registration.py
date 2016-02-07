# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('period_registrations', '0002_periodregistration_section_enrolments'),
        ('students', '0002_student_periods'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentresult',
            name='period_registration',
            field=models.OneToOneField(to='period_registrations.PeriodRegistration'),
            preserve_default=False,
        ),
    ]
